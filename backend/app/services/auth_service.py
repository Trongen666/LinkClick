from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import pyotp
from bson import ObjectId

from app.db.mongo_DB import get_users_collection
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    process_face_image,
    compare_faces,
    generate_otp_secret,
    verify_otp
)
from app.core.config import settings

async def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new user"""
    users = get_users_collection()
    
    # Check if username already exists
    if users.find_one({"username": user_data["username"]}):
        raise ValueError(f"Username {user_data['username']} already exists")
    
    # Check if email already exists
    if users.find_one({"email": user_data["email"]}):
        raise ValueError(f"Email {user_data['email']} already exists")
    
    # Hash password
    hashed_password = get_password_hash(user_data["password"])
    
    # Generate OTP secret
    otp_secret = generate_otp_secret()
    
    # Prepare user document
    user_doc = {
        "username": user_data["username"],
        "email": user_data["email"],
        "full_name": user_data.get("full_name"),
        "hashed_password": hashed_password,
        "face_encoding": None,  # Will be updated later when user adds face
        "otp_secret": otp_secret,
        "failed_login_attempts": 0,
        "last_login": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert user
    result = users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    # Return user without sensitive data
    return format_user_response(user_doc)

async def authenticate_user_password(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user with username and password"""
    users = get_users_collection()
    user = users.find_one({"username": username})
    
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        # Update failed login attempts
        users.update_one(
            {"_id": user["_id"]},
            {"$inc": {"failed_login_attempts": 1}}
        )
        return None
    
    # Reset failed login attempts and update last login
    users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "failed_login_attempts": 0,
                "last_login": datetime.utcnow()
            }
        }
    )
    
    return user

async def authenticate_user_face(username: str, face_image: bytes) -> Dict[str, Any]:
    """Authenticate a user with face recognition"""
    users = get_users_collection()
    user = users.find_one({"username": username})
    
    if not user:
        raise ValueError("User not found")
    
    if not user.get("face_encoding"):
        raise ValueError("User has not set up face authentication")
    
    try:
        # Process the incoming face image
        face_encoding = process_face_image(face_image)
        
        # Compare with stored face encoding
        match = compare_faces(user["face_encoding"], face_encoding)
        
        if not match:
            # Update failed login attempts
            new_attempts = user["failed_login_attempts"] + 1
            users.update_one(
                {"_id": user["_id"]},
                {"$set": {"failed_login_attempts": new_attempts}}
            )
            
            return {
                "success": False,
                "user": format_user_response(user),
                "failed_attempts": new_attempts,
                "should_use_otp": new_attempts >= 2
            }
        
        # Reset failed login attempts and update last login
        users.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "failed_login_attempts": 0,
                    "last_login": datetime.utcnow()
                }
            }
        )
        
        # Generate access token
        access_token = create_access_token(
            subject=str(user["_id"]),
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "success": True,
            "user": format_user_response(user),
            "access_token": access_token
        }
        
    except Exception as e:
        # Handle face processing errors
        return {
            "success": False,
            "error": str(e),
            "user": format_user_response(user),
            "failed_attempts": user["failed_login_attempts"]
        }

async def authenticate_user_otp(username: str, otp: str) -> Dict[str, Any]:
    """Authenticate a user with OTP"""
    users = get_users_collection()
    user = users.find_one({"username": username})
    
    if not user:
        raise ValueError("User not found")
    
    # Verify OTP
    if not verify_otp(user["otp_secret"], otp):
        # Update failed login attempts
        new_attempts = user["failed_login_attempts"] + 1
        users.update_one(
            {"_id": user["_id"]},
            {"$set": {"failed_login_attempts": new_attempts}}
        )
        
        return {
            "success": False,
            "user": format_user_response(user),
            "failed_attempts": new_attempts
        }
    
    # Reset failed login attempts and update last login
    users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "failed_login_attempts": 0,
                "last_login": datetime.utcnow()
            }
        }
    )
    
    # Generate access token
    access_token = create_access_token(
        subject=str(user["_id"]),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "success": True,
        "user": format_user_response(user),
        "access_token": access_token
    }

async def update_user_face(user_id: str, face_image: bytes) -> Dict[str, Any]:
    """Update user's face encoding"""
    users = get_users_collection()
    
    try:
        # Process the face image and get encoding
        face_encoding = process_face_image(face_image)
        
        # Update user's face encoding
        users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "face_encoding": face_encoding.tolist(),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Get updated user
        user = users.find_one({"_id": ObjectId(user_id)})
        
        return format_user_response(user)
    
    except Exception as e:
        raise ValueError(f"Failed to update face: {str(e)}")

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    users = get_users_collection()
    user = users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        return None
    
    return format_user_response(user)

def format_user_response(user: Dict[str, Any]) -> Dict[str, Any]:
    """Format user response to remove sensitive data"""
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user.get("full_name"),
        "has_face_auth": bool(user.get("face_encoding")),
        "failed_login_attempts": user.get("failed_login_attempts", 0),
        "last_login": user.get("last_login"),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }

def get_otp_qr_code_url(username: str) -> str:
    """Get OTP QR code URL for user"""
    users = get_users_collection()
    user = users.find_one({"username": username})
    
    if not user:
        raise ValueError("User not found")
    
    totp = pyotp.TOTP(user["otp_secret"])
    return totp.provisioning_uri(user["email"], issuer_name=settings.PROJECT_NAME)