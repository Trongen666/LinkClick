# """
# Authentication router for the application.
# """
# import base64
# import cv2
# from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Depends
# from fastapi.security import OAuth2PasswordBearer
# from typing import Dict
# from datetime import datetime
# from typing import Optional

# import numpy as np

# from ..services import face2_test

# from ..utils.db import users_collection

# from ..models.user import UserCreate, OTPRequest, OTPVerify, Token
# from ..services.auth_service import (
#     create_access_token,
#     create_user,
#     get_current_active_user,
#     get_user_by_username, 
#     update_face_embedding,
#     request_otp_login, 
#     verify_otp_login,
#     face_login
# )
# from ..services.face_service import extract_face_embedding
# #from ..utils.security import SimpleFaceMatcher

# # In D:\linkclick2\app\routers\auth.py
# from ..services.face2_test import SimpleFaceMatcher


# # Create an instance of SimpleFaceMatcher
# face2_test = SimpleFaceMatcher()


# router = APIRouter(prefix="/auth", tags=["auth"])

# @router.post("/register", status_code=status.HTTP_201_CREATED)
# async def register_user(user: UserCreate):
#     """
#     Register a new user
#     """
#     result = await create_user(user.username, user.phone_number)
#     if not result:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username already exists"
#         )
#     return {"message": "User registered successfully"}

# # @router.post("/register-face", status_code=status.HTTP_200_OK)
# # async def register_face(
# #     username: str = Form(...),
# #     face_image: UploadFile = File(...),
# # ):
# #     """
# #     Register face for a user by username
# #     """
# #     # Read image
# #     image_bytes = await face_image.read()
    
# #     # Extract face embedding
# #     face_embedding = extract_face_embedding(image_bytes)
# #     if not face_embedding:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail="No face detected in the image"
# #         )
    
# #     # Update user with face embedding
# #     success = await update_face_embedding(username, face_embedding)
# #     if not success:
# #         raise HTTPException(
# #             status_code=status.HTTP_404_NOT_FOUND,
# #             detail="User not found or failed to update face embedding"
# #         )
    
# #     return {"message": "Face registered successfully"}

# # @router.post("/register-face", status_code=status.HTTP_201_CREATED)
# # async def register_face(
# #     username: str = Form(...),
# #     face_image: UploadFile = File(...),
# # ):
# #     """
# #     Register a new user with their face and username.
# #     """
# #     # Check if username already exists
# #     existing_user = await get_user_by_username(username)
# #     if existing_user:
# #         raise HTTPException(
# #             status_code=status.HTTP_409_CONFLICT,
# #             detail="Username already exists"
# #         )

# #     # Read the image
# #     image_bytes = await face_image.read()
    
# #     # Extract face embedding
# #     face_embedding = extract_face_embedding(image_bytes)
# #     if not face_embedding:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail="No face detected in the image"
# #         )

#     # Check if the face embedding is already registered (optional)
#     # If you want to check if the face is already registered for another user
#     # existing_face = await get_user_by_face_embedding(face_embedding)
#     # if existing_face:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_409_CONFLICT,
#     #         detail="This face is already registered with another user"
#     #     )

#     # Create new user with the username and face embedding
#     # new_user = {
#     #     "username": username,
#     #     "face_embedding": face_embedding,
#     #     "is_active": True,
#     #     "is_admin": False,  # Change this as needed
#     #     "created_at": datetime.utcnow(),
#     #     "updated_at": datetime.utcnow(),
#     # }

#     # # Store user in the database
#     # result = await users_collection.insert_one(new_user)
#     # new_user["_id"] = result.inserted_id
    
#     # return {"message": "User and face registered successfully", "user": new_user}


# @router.post("/request-otp", status_code=status.HTTP_200_OK)
# async def request_otp(request: OTPRequest):
#     """
#     Request OTP for login
#     """
#     success, message = await request_otp_login(request.username)
#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=message
#         )
    
#     return {"message": message}

# @router.post("/verify-otp", status_code=status.HTTP_200_OK, response_model=Token)
# async def verify_otp(verify: OTPVerify):
#     """
#     Verify OTP and login
#     """
#     success, token_data = await verify_otp_login(verify.username, verify.otp_code)
#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid OTP or username"
#         )
    
#     return token_data

# @router.post("/register-face")
# async def register_face(username: str, face_image: UploadFile = File(...)):    
#     print("Register face endpoint hit!")
#     if await get_user_by_username(username):
#         raise HTTPException(status_code=409, detail="Username already exists")

#     img_bytes = await face_image.read()
#     img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

#     if not face2_test.save_face(img, username):
#         raise HTTPException(status_code=400, detail="No face detected")
    
#     await create_user(username,img)
    
#     test_image = cv2.imread("D://linkclick2//carlos-alcaraz1.jpg")  # Replace with an actual image path
#     embedding = face_matcher.extract_face_embedding(test_image)
#     if embedding is None:
#         return {"message": "Face registered successfully but no embeddings"}

#     else:
#         print(f"Embedding: {embedding}")
#         return {"message": "Face registered successfully, Embedding: {embedding}"}
 

# # @router.post("/register-face", status_code=status.HTTP_201_CREATED)
# # async def register_face(username: str = Form(...), face_image: UploadFile = File(...)):
# #     if await get_user_by_username(username):
# #         raise HTTPException(status_code=409, detail="Username already exists")

# #     img_bytes = await face_image.read()
# #     img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

# #     if not face2_test.save_face(img, username):
# #         raise HTTPException(status_code=400, detail="No face detected")

# #     await create_user(username)
# #     return {"message": "Face registered successfully"}


# # @router.post("/face-login", status_code=status.HTTP_200_OK, response_model=Token)
# # async def login_with_face(
# #     username: str = Form(...),
# #     face_image: UploadFile = File(...)
# # ):
# #     """
# #     Login with face recognition
# #     """
# #     # Read image
# #     image_bytes = await face_image.read()
    
# #     # Try face login
# #     success, token_data = await face_login(username, image_bytes)
# #     if not success:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Face recognition failed"
# #         )
    
# #     return token_data



# # ----------------------------------------------------------------

# # ---------------------------
# # Register using file upload
# # ---------------------------


#    # await create_user(username,img)
#     # return {"message": "Face registered successfully"}





# # @router.get("/get_face_embedding/{username}")
# # async def get_face_embedding(username: str):
# #     """Retrieve the saved face embedding for debugging purposes."""
# #     if username not in face_matcher.face_encodings:
# #         raise HTTPException(status_code=404, detail=f"Face embedding not found for {username}")
    
# #     return {"username": username, "embedding": face_matcher.face_encodings[username].tolist()}

#   # Assuming you have imported SimpleFaceMatcher

# router = APIRouter()

# @router.get("/get_face_embedding/{username}")
# async def get_face_embedding(username: str):
#     """Retrieve the saved face embedding for debugging purposes."""
#     # Fetch the face embedding from MongoDB

#     user = await face_matcher.users_collection.find_one({"username": username})

#     if not user or "face_embedding" not in user:
#         raise HTTPException(status_code=404, detail=f"Face embedding not found for {username}")
    
#     return {"username": username, "embedding": user["face_embedding"]}


# # ---------------------------------
# # Register using base64 image input
# # ---------------------------------
# @router.post("/capture-face", status_code=status.HTTP_200_OK)
# async def capture_face(username: str = Form(...), base64_image: str = Form(...)):
#     if await get_user_by_username(username):
#         raise HTTPException(status_code=409, detail="Username already exists")

#     image_bytes = base64.b64decode(base64_image.split(',')[1] if ',' in base64_image else base64_image)
#     img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

#     if not face2_test.save_face(img, username):
#         raise HTTPException(status_code=400, detail="No face detected")

#     await create_user(username,img)
#     return {"message": "Face captured and registered successfully"}


# # -----------------------
# # Face login via file
# # -----------------------
# # @router.post("/face-login", response_model=Token)
# # async def login_with_face(username: str = Form(...), face_image: UploadFile = File(...)):
# #     user = await get_user_by_username(username)
# #     if not user:
# #         raise HTTPException(status_code=401, detail="User not found")

# #     img_bytes = await face_image.read()
# #     if not face2_test.verify_face_from_image(img_bytes, username):
# #         raise HTTPException(status_code=401, detail="Face mismatch")

# #     access_token = create_access_token({
# #         "sub": username,
# #         "id": str(user["_id"]),
# #         "is_admin": user.get("is_admin", False)
# #     })
# #     return {"access_token": access_token, "token_type": "bearer"}


# # ---------------------------------
# # Timed token-based fallback auth
# # ---------------------------------
# @router.post("/authenticate-timed", response_model=Token)
# async def authenticate_timed(username: str = Form(...)):
#     user = await get_user_by_username(username)
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     access_token = create_access_token({
#         "sub": username,
#         "id": str(user["_id"]),
#         "is_admin": user.get("is_admin", False)
#     })
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/face-login", response_model=Token)
# async def login_with_face(username: str = Form(...), face_image: UploadFile = File(...)):
#     user = await get_user_by_username(username)
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     img_bytes = await face_image.read()
#     if not face2_test.verify_face_from_image(img_bytes, username):
#         raise HTTPException(status_code=401, detail="Face mismatch")

#     access_token = create_access_token({
#         "sub": username,
#         "id": str(user["_id"]),
#         "is_admin": user.get("is_admin", False)
#     })
#     return {"access_token": access_token, "token_type": "bearer"}

# # ----------------------------
# # Get current logged-in user
# # ----------------------------
# @router.post("/verify-user")
# async def verify_user(user: dict = Depends(get_current_active_user)):
#     return {"username": user["username"], "is_active": user["is_active"]}



"""
Authentication router for the application.
"""
import base64
import cv2
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from datetime import datetime
from typing import Optional

import numpy as np

from ..services import face2_test

from ..utils.db import users_collection

from ..models.user import UserCreate, OTPRequest, OTPVerify, Token
from ..services.auth_service import (
    create_access_token,
    create_user,
    get_current_active_user,
    get_user_by_username, 
    update_face_embedding,
    request_otp_login, 
    verify_otp_login,
    face_login
)
from ..services.face_service import extract_face_embedding
#from ..utils.security import SimpleFaceMatcher

# In D:\linkclick2\app\routers\auth.py
from ..services.face2_test import SimpleFaceMatcher


# Create an instance of SimpleFaceMatcher
face2_test = SimpleFaceMatcher()

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


@router.post("/register-face")
async def register_face(username: str = Form(...), face_image: UploadFile = File(...)):    
    print("Register face endpoint hit!")

    if await get_user_by_username(username):
        raise HTTPException(status_code=409, detail="Username already exists")

    img_bytes = await face_image.read()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image data")

    success, embedding = await face2_test.save_face(img, username)
    if not success:
        raise HTTPException(status_code=400, detail="No face detected or embedding failed")

    await create_user(username, None)

    return {
        "message": "Face registered successfully",
        "embedding": embedding.tolist()
    }


# async def register_face(username: str = Form(...), face_image: UploadFile = File(...)):    
#     print("Register face endpoint hit!")
#     if await get_user_by_username(username):
#         raise HTTPException(status_code=409, detail="Username already exists")

#     img_bytes = await face_image.read()
#     img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

#     if not face2_test.save_face(img, username):
#         raise HTTPException(status_code=400, detail="No face detected")
    
#     await create_user(username, None)
#     return {"message": "Face registered successfully"}

# @router.get("/get_face_embedding/{username}")
# async def get_face_embedding(username: str):
#     """Retrieve the saved face embedding for debugging purposes."""
#     user = await face_matcher.users_collection.find_one({"username": username})

#     if not user or "face_embedding" not in user:
#         raise HTTPException(status_code=404, detail=f"Face embedding not found for {username}")
    
#     return {"username": username, "embedding_exists": True}

@router.post("/capture-face", status_code=status.HTTP_200_OK)
async def capture_face(username: str = Form(...), base64_image: str = Form(...)):
    if await get_user_by_username(username):
        raise HTTPException(status_code=409, detail="Username already exists")

    try:
        # Handle data URI format if present
        if ',' in base64_image:
            image_bytes = base64.b64decode(base64_image.split(',')[1])
        else:
            image_bytes = base64.b64decode(base64_image)
            
        img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid base64 image data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error decoding base64 image: {str(e)}")

    if not face2_test.save_face(img, username):
        raise HTTPException(status_code=400, detail="No face detected")

    await create_user(username, None)
    return {"message": "Face captured and registered successfully"}

@router.post("/face-login", response_model=Token)
async def login_with_face(username: str = Form(...), face_image: UploadFile = File(...)):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    img_bytes = await face_image.read()
    if not face2_test.verify_face_from_image(img_bytes, username):
        raise HTTPException(status_code=401, detail="Face mismatch")

    access_token = create_access_token({
        "sub": username,
        "id": str(user["_id"]),
        "is_admin": user.get("is_admin", False)
    })
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/authenticate-timed", response_model=Token)
async def authenticate_timed(username: str = Form(...)):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_access_token({
        "sub": username,
        "id": str(user["_id"]),
        "is_admin": user.get("is_admin", False)
    })
    return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/verify-token")
# async def verify_token(user: dict ):
#     return {
#         "username": user["username"],
#         "is_active": user["is_active"],
#         "valid_token": True
#     }



# @router.get("/admin-only")
# async def admin_only(user: dict = Depends(get_current_active_user)):
#     if not user.get("is_admin"):
#         raise HTTPException(status_code=403, detail="Access denied: Admins only")
    
#     return {"message": f"Welcome, admin {user['username']}"}

# @router.get("/session-info")
# async def session_info(user: dict = Depends(get_current_active_user)):
#     return {
#         "username": user["username"],
#         "is_admin": user.get("is_admin", False),
#         "user_id": str(user["_id"]),
#         "phone_number": user.get("phone_number"),
#         "is_active": user["is_active"]
#     }

