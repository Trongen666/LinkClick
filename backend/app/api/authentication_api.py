from fastapi import APIRouter, HTTPException, Depends, status, File, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, Any
from datetime import timedelta
from jose import jwt, JWTError
from bson import ObjectId

from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import UserCreate, User, Token, OTPLoginRequest, LoginResponse, LoginFailureResponse
from app.services.auth_service import (
    create_user, 
    authenticate_user_password,
    authenticate_user_face,
    authenticate_user_otp,
    update_user_face,
    get_user_by_id,
    get_otp_qr_code_url
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        user = await create_user(user_data.dict())
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login/password", response_model=Token)
async def login_password(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with username and password"""
    user = await authenticate_user_password(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        subject=str(user["_id"]),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "full_name": user.get("full_name"),
            "has_face_auth": bool(user.get("face_encoding"))
        }
    }

@router.post("/login/face", response_model=LoginResponse)
async def login_face(
    username: str = Form(...),
    face_image: UploadFile = File(...)
):
    """Login with face recognition"""
    try:
        image_bytes = await face_image.read()
        result = await authenticate_user_face(username, image_bytes)
        
        if not result["success"]:
            response = LoginFailureResponse(
                detail="Face authentication failed",
                remaining_attempts=3 - result["failed_attempts"],
                should_use_otp=result["should_use_otp"]
            )
            return response
        
        return LoginResponse(
            user=result["user"],
            access_token=result["access_token"]
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Face authentication error: {str(e)}"
        )

@router.post("/login/otp", response_model=LoginResponse)
async def login_otp(login_data: OTPLoginRequest):
    """Login with OTP"""
    try:
        result = await authenticate_user_otp(login_data.username, login_data.otp)
        
        if not result["success"]:
            response = LoginFailureResponse(
                detail="Invalid OTP",
                remaining_attempts=3 - result["failed_attempts"],
                should_use_otp=True
            )
            return response
        
        return LoginResponse(
            user=result["user"],
            access_token=result["access_token"]
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/update-face", response_model=User)
async def update_face(
    face_image: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update user's face for authentication"""
    try:
        image_bytes = await face_image.read()
        updated_user = await update_user_face(current_user["id"], image_bytes)
        return updated_user
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=User)
async def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user details"""
    return current_user

@router.get("/otp-qr-code")
async def get_otp_qr_code(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get OTP QR code for user"""
    try:
        qr_code_url = get_otp_qr_code_url(current_user["username"])
        return {"qr_code_url": qr_code_url}
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )