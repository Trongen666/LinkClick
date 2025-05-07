from fastapi import APIRouter
from app.models.notification import NotificationRequest
from app.services.notification_service import handle_notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/")
def create_notification(notification: NotificationRequest):
    return handle_notification(notification)