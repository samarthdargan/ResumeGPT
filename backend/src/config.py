from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME: str = "ResumeGPT"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    CORS_ORIGINS: List[str] = ["*"]
    CLERK_JWKS_URL: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
