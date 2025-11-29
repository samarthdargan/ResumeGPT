from pydantic_settings import BaseSettings
from typing import List, Optional, Union
from pydantic import field_validator

class Settings(BaseSettings):
    APP_NAME: str = "ResumeGPT"
    VERSION: str = "0.1.0"
    DEBUG: bool = False
    CORS_ORIGINS: Union[List[str], str] = ["*"]
    CLERK_JWKS_URL: Optional[str] = None

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        env_file = ".env"

settings = Settings()
