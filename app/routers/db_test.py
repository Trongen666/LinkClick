from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta
from bson import ObjectId
from ..utils.db import users_collection, otp_collection, login_attempts_collection, sessions_collection

router = APIRouter(prefix="/debug", tags=["debug"])

@router.post("/test-user")
async def insert_test_user(username: str, phone_number: str):
    """Insert a test user document into MongoDB"""
    user_data = {
        "username": username,
        "phone_number": phone_number,
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "face_embedding": None
    }
    try:
        result = await users_collection.insert_one(user_data)
        return {"message": "User inserted", "user_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-otp")
async def insert_test_otp(username: str, otp_code: str):
    """Insert a test OTP with TTL"""
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    otp_data = {
        "username": username,
        "otp_code": otp_code,
        "expires_at": expires_at
    }
    try:
        await otp_collection.replace_one(
            {"username": username},
            otp_data,
            upsert=True
        )
        return {"message": "OTP inserted", "expires_at": expires_at}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-login-attempt")
async def insert_login_attempt(username: str, ip: str):
    """Insert a login attempt (expires after 7 days automatically)"""
    attempt_data = {
        "username": username,
        "ip_address": ip,
        "timestamp": datetime.utcnow()
    }
    try:
        result = await login_attempts_collection.insert_one(attempt_data)
        return {"message": "Login attempt recorded", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-session")
async def insert_session(user_id: str, token: str):
    """Insert a session with expiry"""
    expires_at = datetime.utcnow() + timedelta(days=1)
    session_data = {
        "user_id": ObjectId(user_id),
        "token": token,
        "expires_at": expires_at
    }
    try:
        result = await sessions_collection.insert_one(session_data)
        return {"message": "Session created", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check-collections")
async def check_collection_counts():
    """Check document counts in all main collections"""
    try:
        counts = {
            "users": await users_collection.count_documents({}),
            "otps": await otp_collection.count_documents({}),
            "login_attempts": await login_attempts_collection.count_documents({}),
            "sessions": await sessions_collection.count_documents({}),
        }
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
