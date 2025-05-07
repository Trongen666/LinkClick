from pydantic import BaseModel, Field
from typing import Literal

class NotificationRequest(BaseModel):
    user_id: int
    message: str
    method: Literal["email", "in_app"]
    duration: int = Field(..., description="Duration of notification in minutes")