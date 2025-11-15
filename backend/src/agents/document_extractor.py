import base64
from pathlib import Path
from openai import AsyncAzureOpenAI
from ..config import settings
import json
import docx2pdf
from pdf2image import convert_from_path
from io import BytesIO
import re
import logging

logger = logging.getLogger(__name__)


class DocumentExtractor:
    def __init__(self):
        # Use official Azure OpenAI client for vision support
        self.openai_client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version="2024-02-15-preview",  # Vision-enabled API version
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        self.deployment_name = settings.AZURE_OPENAI_DEPLOYMENT_NAME

    async def extract_from_file(self, file_path: str) -> dict:
        """Extract structured information from the resume document at file_path"""
        logger.info(f"📄 Extracting from file: {file_path}")
        path = Path(file_path)
        
        if not path.exists():
            return {"success": False, "error": "File not found"}
        
        extension = path.suffix.lower()
        logger.info(f"📎 File extension: {extension}")
        images_b64 = []

        try:
            if extension == ".pdf":
                logger.info("🔄 Converting PDF to images...")
                images = convert_from_path(file_path, dpi=300, fmt='jpeg')
                logger.info(f"✅ Converted PDF to {len(images)} images")
                
                # Process up to 5 pages
                for idx, img in enumerate(images[:5]):
                    logger.info(f"  Processing page {idx + 1}...")
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG", quality=95)
                    img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    images_b64.append(img_b64)
                    
                    img_size_kb = len(img_b64) / 1024
                    logger.info(f"  Page {idx + 1} size: {img_size_kb:.2f} KB")
                    
            elif extension in {".docx", ".doc"}:
                logger.info("🔄 Converting DOCX to PDF...")
                temp_pdf_path = path.with_suffix(".pdf")
                docx2pdf.convert(str(file_path), str(temp_pdf_path))
                
                images = convert_from_path(str(temp_pdf_path), dpi=300, fmt='jpeg')
                logger.info(f"✅ Converted to {len(images)} images")
                
                for idx, img in enumerate(images[:5]):
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG", quality=95)
                    img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    images_b64.append(img_b64)
                    
                if temp_pdf_path.exists():
                    temp_pdf_path.unlink()
                    
            elif extension == ".txt":
                logger.info("📝 Reading text file...")
                with open(file_path, "r", encoding="utf-8") as f:
                    text_content = f.read()
                logger.info(f"✅ Read {len(text_content)} characters")
                return await self.extract_from_text(text_content)
                
            elif extension in [".jpg", ".jpeg", ".png"]:
                logger.info("🖼️ Reading image file...")
                with open(file_path, "rb") as f:
                    img_b64 = base64.b64encode(f.read()).decode('utf-8')
                    images_b64.append(img_b64)
                logger.info(f"✅ Image size: {len(img_b64) / 1024:.2f} KB")
            else:
                return {"success": False, "error": f"Unsupported file type: {extension}"}
            
            if not images_b64:
                return {"success": False, "error": "No images were extracted from the file"}
            
            logger.info(f"🚀 Sending {len(images_b64)} images to AI for extraction...")
            extracted_data = await self.extract_from_images(images_b64)
            return extracted_data
            
        except Exception as e:
            logger.error(f"❌ Error during extraction: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"Extraction failed: {str(e)}"}
    
    async def extract_from_images(self, images_b64: list) -> dict:
        """Extract structured information from base64 encoded images of the resume"""
        
        # Build message content with images
        user_content = []
        
        for idx, img_b64 in enumerate(images_b64):
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_b64}",
                    "detail": "high"  # Use high detail for better OCR
                }
            })
        
        # Add text instruction
        user_content.append({
            "type": "text",
            "text": """Extract all information from these resume images into comprehensive JSON format.

CRITICAL INSTRUCTIONS:
1. READ all text visible in the images carefully
2. Extract ONLY information that is ACTUALLY PRESENT
3. DO NOT make up or fabricate any information
4. If something is unclear or not visible, use null
5. Preserve EXACT wording from the document

Return JSON with this structure:
{
  "personal_info": {
    "name": "",
    "email": "",
    "phone": "",
    "address": "",
    "linkedin": "",
    "github": "",
    "portfolio_links": [],
    "other_links": []
  },
  "professional_summary": {
    "full_text": "",
    "key_points": []
  },
  "experience": [
    {
      "job_title": "",
      "company_name": "",
      "location": "",
      "dates": "",
      "bullet_points": [],
      "technologies": [],
      "metrics": []
    }
  ],
  "skills": {
    "technical_skills": [],
    "soft_skills": [],
    "tools": [],
    "frameworks": [],
    "languages": []
  },
  "education": [
    {
      "institution": "",
      "degree": "",
      "field": "",
      "dates": "",
      "honors": "",
      "coursework": []
    }
  ],
  "projects": [
    {
      "name": "",
      "description": "",
      "technologies": [],
      "role": "",
      "outcomes": []
    }
  ],
  "certifications": [
    {
      "name": "",
      "organization": "",
      "date": ""
    }
  ],
  "additional_sections": {
    "publications": [],
    "volunteer_work": [],
    "interests": [],
    "references": null
  }
}

OUTPUT RULES:
- Return ONLY valid JSON
- NO markdown code blocks (no ```json or ```)
- NO explanatory text before or after
- Start directly with { and end with }
- Use null for missing fields, not fake data"""
        })
        
        # Build complete message structure
        messages = [
            {
                "role": "system",
                "content": "You are an expert resume parser with advanced OCR capabilities. Extract all visible text accurately and comprehensively. Never fabricate information."
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
        
        logger.info(f"📤 Calling Azure OpenAI with {len(images_b64)} images...")
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=4000,
                temperature=0.1  # Low temperature for more consistent extraction
            )
            
            response_text = response.choices[0].message.content
            
            logger.info(f"📥 Received response (length: {len(response_text)} chars)")
            logger.info(f"📄 First 300 chars: {response_text[:300]}")
            
            # Clean and parse JSON
            cleaned_response = self._clean_json_response(response_text)
            
            try:
                extracted_json = json.loads(cleaned_response)
                
                logger.info("✅ Successfully extracted and parsed JSON")
                return {
                    "success": True,
                    "extracted_data": extracted_json,
                    "pages_processed": len(images_b64),
                    "method": "multimodal_vision"
                }
                
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON parsing failed: {e}")
                logger.error(f"Attempted to parse: {cleaned_response[:300]}")
                return {
                    "success": False,
                    "error": f"Invalid JSON response: {str(e)}",
                    "raw_response": response_text[:1000]
                }
                
        except Exception as e:
            logger.error(f"❌ API call failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"API error: {str(e)}"}
    
    async def extract_from_text(self, text_content: str) -> dict:
        """Extract structured information from plain text resume content"""
        
        if not text_content or len(text_content.strip()) < 50:
            return {
                "success": False,
                "error": "Text content is too short or empty"
            }
        
        logger.info(f"📝 Extracting from text ({len(text_content)} chars)")
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert resume parser. Extract all information accurately without fabricating data."
            },
            {
                "role": "user",
                "content": f"""Extract all information from this resume text into comprehensive JSON format.

RESUME TEXT:
{text_content}

Return JSON with this structure:
{{
  "personal_info": {{"name": "", "email": "", "phone": "", ...}},
  "professional_summary": {{"full_text": "", "key_points": []}},
  "experience": [...],
  "skills": {{}},
  "education": [...],
  "projects": [...],
  "certifications": [...],
  "additional_sections": {{}}
}}

RULES:
- Extract ONLY information present in the text
- Use exact wording from the resume
- Use null for missing fields
- Return ONLY valid JSON (no markdown, no explanations)"""
            }
        ]
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=4000,
                temperature=0.1
            )
            
            response_text = response.choices[0].message.content
            cleaned = self._clean_json_response(response_text)
            extracted_json = json.loads(cleaned)
            
            logger.info("✅ Successfully extracted from text")
            return {
                "success": True,
                "extracted_data": extracted_json,
                "method": "text_extraction"
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed: {e}")
            return {
                "success": False,
                "error": f"Invalid JSON: {str(e)}",
                "raw_response": response_text[:1000]
            }
        except Exception as e:
            logger.error(f"❌ Extraction failed: {str(e)}")
            return {
                "success": False,
                "error": f"Extraction failed: {str(e)}"
            }
    
    def _clean_json_response(self, text: str) -> str:
        """Remove markdown formatting and extract JSON"""
        cleaned = text.strip()
        
        # Remove markdown code blocks
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        
        # Find JSON object boundaries
        start = cleaned.find('{')
        end = cleaned.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start:end+1]
        
        return cleaned