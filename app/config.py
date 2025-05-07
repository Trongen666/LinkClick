import os
import secrets
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator, AnyHttpUrl
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Authentication System"
    VERSION: str = "1.0.0"

    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # MongoDB
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "auth_system")

    # OTP Settings
    OTP_LENGTH: int = 6
    OTP_EXPIRATION_MINUTES: int = 5

    # Face Recognition
    FACE_RECOGNITION_THRESHOLD: float = 0.6  # <-- changed name to match import

    # Twilio
    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: Optional[str] = os.getenv("TWILIO_PHONE_NUMBER", "")

    # File upload
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads/")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Admin user
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PHONE_NUMBER: str = os.getenv("ADMIN_PHONE_NUMBER", "1234567890")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Rate limiting
    RATE_LIMIT_LOGIN_ATTEMPTS: int = 5

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # <-- allow extra fields in environment

# Instantiate settings
settings = Settings()
