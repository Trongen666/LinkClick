"""
User management router for the application.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, List
from datetime import datetime
from bson import ObjectId

from ..models.user import User, UserInDB
from ..utils.db import users_collection
from ..utils.security import get_current_user, get_current_admin

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """
    Get current user info
    """
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "phone_number": current_user["phone_number"],
        "is_active": current_user["is_active"],
        "is_admin": current_user["is_admin"],
        "created_at": current_user["created_at"],
        "updated_at": current_user["updated_at"]
    }

@router.get("/", response_model=List[User])
async def get_all_users(current_user: Dict = Depends(get_current_admin)):
    """
    Get all users (admin only)
    """
    users = []
    async for user in users_collection.find():
        users.append({
            "id": str(user["_id"]),
            "username": user["username"],
            "phone_number": user["phone_number"],
            "is_active": user["is_active"],
            "is_admin": user["is_admin"],
            "created_at": user["created_at"],
            "updated_at": user["updated_at"]
        })
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, current_user: Dict = Depends(get_current_admin)):
    """
    Get user by ID (admin only)
    """
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
        
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "phone_number": user["phone_number"],
        "is_active": user["is_active"],
        "is_admin": user["is_admin"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }

@router.put("/{user_id}/activate", status_code=status.HTTP_200_OK)
async def activate_user(user_id: str, current_user: Dict = Depends(get_current_admin)):
    """
    Activate user (admin only)
    """
    try:
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "is_active": True,
                "updated_at": datetime.utcnow()
            }}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
        
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return {"message": "User activated successfully"}

@router.put("/{user_id}/deactivate", status_code=status.HTTP_200_OK)
async def deactivate_user(user_id: str, current_user: Dict = Depends(get_current_admin)):
    """
    Deactivate user (admin only)
    """
    try:
        # Prevent deactivating self
        if str(current_user["_id"]) == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate yourself"
            )
            
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "is_active": False,
                "updated_at": datetime.utcnow()
            }}
        )
    except HTTPException:
        raise
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
        
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return {"message": "User deactivated successfully"}

@router.put("/{user_id}/make-admin", status_code=status.HTTP_200_OK)
async def make_admin(user_id: str, current_user: Dict = Depends(get_current_admin)):
    """
    Make user an admin (admin only)
    """
    try:
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "is_admin": True,
                "updated_at": datetime.utcnow()
            }}
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
        
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return {"message": "User granted admin privileges"}

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, current_user: Dict = Depends(get_current_admin)):
    """
    Delete user (admin only)
    """
    try:
        # Prevent deleting self
        if str(current_user["_id"]) == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete yourself"
            )
            
        result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    except HTTPException:
        raise
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )
        
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return {"message": "User deleted successfully"}