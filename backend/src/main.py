# Main FastAPI Application"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import settings


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


