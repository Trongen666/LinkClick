# import os
# from dotenv import load_dotenv

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# JWT_SECRET = os.getenv("JWT_SECRET")

import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Futuristic Auth System"
    
    MONGODB_URL: str = os.getenv("MONGODB_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Face recognition settings
    FACE_RECOGNITION_DIR: str = "app/data/faces"
    FACE_RECOGNITION_THRESHOLD: float = float(os.getenv("FACE_RECOGNITION_THRESHOLD", "0.6"))

    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"]

# Create settings instance
settings = Settings()

# Ensure face recognition directory exists
os.makedirs(settings.FACE_RECOGNITION_DIR, exist_ok=True)

