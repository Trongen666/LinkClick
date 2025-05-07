"""
Security utilities for authentication and authorization.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from ..models.user import TokenData
from ..utils.db import users_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_access_token(data: Dict) -> str:
    """
    Create a new JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """
    Decode and validate the current user's JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id, is_admin=payload.get("is_admin", False))
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = await users_collection.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
        
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
        
    return user

async def get_current_admin(current_user: Dict = Depends(get_current_user)) -> Dict:
    """
    Check if current user is an admin
    """
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user