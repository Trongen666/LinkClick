# from datetime import datetime, timedelta
# from typing import Any, Union, Optional

# import face_recognition
# import numpy as np
# import pyotp
# import base64
# from jose import jwt
# from passlib.context import CryptContext
# from PIL import Image
# from io import BytesIO

# from app.core.config import settings

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # OTP generation
# def generate_otp_secret():
#     """Generate a secure OTP secret"""
#     return pyotp.random_base32()

# def verify_otp(secret: str, otp: str) -> bool:
#     """Verify OTP code"""
#     totp = pyotp.TOTP(secret)
#     return totp.verify(otp)

# # Password functions
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a password against a hash"""
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password: str) -> str:
#     """Hash a password"""
#     return pwd_context.hash(password)

# # JWT token functions
# def create_access_token(
#     subject: Union[str, Any], expires_delta: Optional[timedelta] = None
# ) -> str:
#     """Create a JWT access token"""
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
#         )
    
#     to_encode = {"exp": expire, "sub": str(subject)}
#     encoded_jwt = jwt.encode(
#         to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
#     )
#     return encoded_jwt

# # Face recognition functions
# def process_face_image(image_data: bytes) -> np.ndarray:
#     """Process image data and extract face encodings"""
#     image = Image.open(BytesIO(image_data))
#     image_np = np.array(image)
#     face_locations = face_recognition.face_locations(image_np)
    
#     if not face_locations:
#         raise ValueError("No face detected in the image")
    
#     face_encodings = face_recognition.face_encodings(image_np, face_locations)
#     if not face_encodings:
#         raise ValueError("Could not encode face in the image")
    
#     return face_encodings[0]

# def compare_faces(known_encoding: list[float], new_encoding: np.ndarray) -> bool:
#     """Compare face encodings and determine if they match"""
#     if not known_encoding:
#         return False
    
#     # Convert stored encoding back to numpy array
#     known_encoding_np = np.array(known_encoding)
    
#     # Calculate face distance
#     face_distance = face_recognition.face_distance([known_encoding_np], new_encoding)[0]
    
#     # Return True if the distance is below threshold (lower distance = better match)
#     return face_distance < settings.FACE_RECOGNITION_THRESHOLD

from datetime import datetime, timedelta
from typing import Any, Union, Optional
import numpy as np
import pyotp
import base64
from jose import jwt
from passlib.context import CryptContext
from PIL import Image
from io import BytesIO

import mediapipe as mp
from insightface.app import FaceAnalysis

from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OTP generation
def generate_otp_secret():
    """Generate a secure OTP secret"""
    return pyotp.random_base32()

def verify_otp(secret: str, otp: str) -> bool:
    """Verify OTP code"""
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

# Password functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

# JWT token functions
def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

# ---------- Face Recognition Section (Refactored) ----------

# InsightFace setup (you can move this to a module-level initializer)
face_app = FaceAnalysis(name='buffalo_l')  # You can choose other models if needed
face_app.prepare(ctx_id=0)  # Set ctx_id=-1 for CPU only

def process_face_image(image_data: bytes) -> np.ndarray:
    """Process image data and extract face encodings"""
    image = Image.open(BytesIO(image_data)).convert("RGB")
    image_np = np.array(image)

    # Detect and embed using InsightFace
    faces = face_app.get(image_np)
    if not faces:
        raise ValueError("No face detected in the image")

    return faces[0].embedding  # Return embedding vector

def compare_faces(known_encoding: list[float], new_encoding: np.ndarray) -> bool:
    """Compare face encodings and determine if they match"""
    if not known_encoding:
        return False

    known_encoding_np = np.array(known_encoding)
    distance = np.linalg.norm(known_encoding_np - new_encoding)

    return distance < settings.FACE_RECOGNITION_THRESHOLD  # e.g. 1.0
