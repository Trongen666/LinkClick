"""
Authentication router for the application.
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict

from ..models.user import UserCreate, OTPRequest, OTPVerify, Token
from ..services.auth_service import (
    create_user, 
    update_face_embedding,
    request_otp_login, 
    verify_otp_login,
    face_login
)
from ..services.face_service import extract_face_embedding
from ..utils.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """
    Register a new user
    """
    result = await create_user(user.username, user.phone_number)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    return {"message": "User registered successfully"}

# @router.post("/register-face", status_code=status.HTTP_200_OK)
# async def register_face(
#     username: str = Form(...),
#     face_image: UploadFile = File(...),
# ):
#     """
#     Register face for a user by username
#     """
#     # Read image
#     image_bytes = await face_image.read()
    
#     # Extract face embedding
#     face_embedding = extract_face_embedding(image_bytes)
#     if not face_embedding:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="No face detected in the image"
#         )
    
#     # Update user with face embedding
#     success = await update_face_embedding(username, face_embedding)
#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found or failed to update face embedding"
#         )
    
#     return {"message": "Face registered successfully"}

@router.post("/register-face", status_code=status.HTTP_201_CREATED)
async def register_face(
    username: str = Form(...),
    face_image: UploadFile = File(...),
):
    """
    Register a new user with their face and username.
    """
    # Check if username already exists
    existing_user = await get_user_by_username(username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # Read the image
    image_bytes = await face_image.read()
    
    # Extract face embedding
    face_embedding = extract_face_embedding(image_bytes)
    if not face_embedding:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No face detected in the image"
        )

    # Check if the face embedding is already registered (optional)
    # If you want to check if the face is already registered for another user
    existing_face = await get_user_by_face_embedding(face_embedding)
    if existing_face:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This face is already registered with another user"
        )

    # Create new user with the username and face embedding
    new_user = {
        "username": username,
        "face_embedding": face_embedding,
        "is_active": True,
        "is_admin": False,  # Change this as needed
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    # Store user in the database
    result = await users_collection.insert_one(new_user)
    new_user["_id"] = result.inserted_id
    
    return {"message": "User and face registered successfully", "user": new_user}


@router.post("/request-otp", status_code=status.HTTP_200_OK)
async def request_otp(request: OTPRequest):
    """
    Request OTP for login
    """
    success, message = await request_otp_login(request.username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return {"message": message}

@router.post("/verify-otp", status_code=status.HTTP_200_OK, response_model=Token)
async def verify_otp(verify: OTPVerify):
    """
    Verify OTP and login
    """
    success, token_data = await verify_otp_login(verify.username, verify.otp_code)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP or username"
        )
    
    return token_data

@router.post("/face-login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_with_face(
    username: str = Form(...),
    face_image: UploadFile = File(...)
):
    """
    Login with face recognition
    """
    # Read image
    image_bytes = await face_image.read()
    
    # Try face login
    success, token_data = await face_login(username, image_bytes)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Face recognition failed"
        )
    
    return token_data