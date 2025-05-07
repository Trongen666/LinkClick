from app.models.notification import NotificationRequest

def handle_notification(notification: NotificationRequest):
    # Dummy implementation
    return {
        "status": "success",
        "user_id": notification.user_id,
        "method": notification.method,
        "duration": notification.duration,
        "message": notification.message
    }