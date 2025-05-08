from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl, Field
from typing import List
from datetime import date
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# MongoDB setup
client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]
tutorials_collection = db.tutorials

# Models
class TutorialItem(BaseModel):
    description: str
    videoLink: HttpUrl
    uploadedBy: str
    uploadedDate: date
    thumbnail: HttpUrl

class TutorialCategory(BaseModel):
    tutorialCategory: str = Field(..., example="Transport")
    tutorials: List[TutorialItem]


@router.post("/api/tutorials/", status_code=201)
async def add_tutorial_category(tutorial_data: TutorialCategory):
    try:
        result = await tutorials_collection.insert_one(tutorial_data.dict())
        return {"message": "Tutorial category added", "id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Failed to insert tutorial: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
