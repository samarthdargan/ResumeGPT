# Main FastAPI Application"

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from .agents.test_agent import TestAgent
from .agents.document_extractor import DocumentExtractor
from .config import settings
from pathlib import Path
import aiofiles

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
TEMPLATES_UPLOAD_DIR = Path("templates")
UPLOAD_DIR.mkdir(exist_ok=True)
TEMPLATES_UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "ready"
    }

@app.get("/health")
async def health():
    "Health check endpoint"
    return {"status": "healthy"}

@app.get("/test-agent")
async def test_agent():
    "Endpoint to test the TestAgent connection"
    agent = TestAgent()
    result = await agent.test_connection()
    return result
    
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload and extract data from a resume file"""
    
    allowed_extensions = {".pdf", ".docx", ".txt", ".doc", ".png", ".jpg", ".jpeg"}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}"
        )
    
    contents = await file.read()
    
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    file_path = UPLOAD_DIR / file.filename
    
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(contents)
        
        if not file_path.exists() or file_path.stat().st_size == 0:
            raise HTTPException(status_code=500, detail="Failed to save file")
        
        print(f"✅ File saved: {file_path} ({len(contents)} bytes)")
        
        extractor = DocumentExtractor()
        result = await extractor.extract_from_file(str(file_path))
        
        print(f"📊 Extraction completed: {result.get('success', False)}")
        
        return {
            "filename": file.filename,
            "size": len(contents),
            "extraction": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    finally:
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"🗑️ Cleaned up: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to delete file: {e}")

@app.post("/process")
async def process_resume(file: UploadFile = File(...),template_id: int = 1):
    """Endpoint to process the uploaded resume and convert to LaTeX"""
    from .agents.latex_converter import LaTeXConverter

    
    content = await upload_file(file)
    content = content.get("extraction", {})
    if not content.get("success", False):
        return {"success": False, "error": content.get("error", "Unknown upload error")}
    content = content.get("extracted_data", {})
    
    try:
        latex_file_path = TEMPLATES_UPLOAD_DIR / f"{template_id}.tex"
        async with aiofiles.open(latex_file_path, mode='r') as f:
            latex_template = await f.read()
   
        converter = LaTeXConverter()
        latex_result = await converter.convert_to_latex(latex_template=latex_template,json_data=content)
        
        if not latex_result.get("success", False):
            return {
                     "success": False,
                     "error": f"Error: {str(e)}",
                 }
           
        else:
            latex_filename = f"{Path(file.filename).stem}.tex"
            latex_path = UPLOAD_DIR / latex_filename
            async with aiofiles.open(latex_path, 'w') as latex_file:
                await latex_file.write(latex_result.get("latex", ""))

            return {
                "success": True,
                "original_filename": file.filename,
                "extracted_data": content,
                "latex_filename": latex_filename,
                "lates_path": str(latex_path),
                "latex_preview": latex_result.get("latex", "")[:500]  # First 500 chars
            }
    except HTTPException:
        return {"success": False, "error": he.detail}
    except Exception as e:
        return {"success": False, "error": f"LaTeX conversion error: {str(e)}"}