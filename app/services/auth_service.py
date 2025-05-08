# """
# Authentication service for the application.
# """
# from datetime import datetime
# from typing import Dict, Optional, Tuple

# from ..utils.db import users_collection
# from ..utils.security import create_access_token
# from ..services.otp import generate_otp, verify_otp, send_otp_to_phone
# from ..services.face_service import extract_face_embedding, verify_face

# async def create_user(username: str, phone_number: str) -> Dict:
#     """
#     Create a new user
#     """
#     # Check if user exists
#     existing_user = await users_collection.find_one({"username": username})
#     if existing_user:
#         return None
        
#     # Create new user
#     user = {
#         "username": username,
#         "phone_number": phone_number,
#         "is_active": True,
#         "is_admin": False,
#         "face_embedding": None,
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow()
#     }
    
#     # Insert user to database
#     result = await users_collection.insert_one(user)
#     user["_id"] = result.inserted_id
    
#     return user

# async def update_face_embedding(username: str, face_embedding: list) -> bool:
#     """
#     Update face embedding for a user
#     """
#     result = await users_collection.update_one(
#         {"username": username},
#         {"$set": {
#             "face_embedding": face_embedding,
#             "updated_at": datetime.utcnow()
#         }}
#     )
    
#     return result.modified_count > 0

# async def request_otp_login(username: str) -> Tuple[bool, str]:
#     """
#     Request OTP login for a user
#     Returns: (success, message)
#     """
#     # Find user
#     user = await users_collection.find_one({"username": username})
#     if not user:
#         return False, "User not found"
        
#     # Generate OTP
#     otp = await generate_otp(username)
    
#     # Send OTP to user's phone
#     sent = await send_otp_to_phone(user["phone_number"], otp)
#     if not sent:
#         return False, "Failed to send OTP"
        
#     return True, "OTP sent successfully"

# async def verify_otp_login(username: str, otp: str) -> Tuple[bool, Optional[Dict]]:
#     """
#     Verify OTP login for a user
#     Returns: (success, token_data)
#     """
#     # Find user
#     user = await users_collection.find_one({"username": username})
#     if not user:
#         return False, None
        
#     # Verify OTP
#     is_valid = await verify_otp(username, otp)
#     if not is_valid:
#         return False, None
        
#     # Create token
#     token_data = {
#         "sub": user["username"],
#         "id": str(user["_id"]),
#         "is_admin": user.get("is_admin", False)
#     }
    
#     token = create_access_token(token_data)
    
#     return True, {"access_token": token, "token_type": "bearer"}

# async def face_login(username: str, face_image: bytes) -> Tuple[bool, Optional[Dict]]:
#     """
#     Login with face recognition
#     Returns: (success, token_data)
#     """
#     # Find user
#     user = await users_collection.find_one({"username": username})
#     if not user:
#         return False, None
        
#     # Check if user has face embedding
#     if not user.get("face_embedding"):
#         return False, None
        
#     # Extract face embedding from image
#     new_embedding = extract_face_embedding(face_image)
#     if not new_embedding:
#         return False, None
        
#     # Verify face
#     is_valid = verify_face(user["face_embedding"], new_embedding)
#     if not is_valid:
#         return False, None
        
#     # Create token
#     token_data = {
#         "sub": user["username"],
#         "id": str(user["_id"]),
#         "is_admin": user.get("is_admin", False)
#     }
    
#     token = create_access_token(token_data)
    
#     return True, {"access_token": token, "token_type": "bearer"}

# """
# OTP generation and verification service with Twilio integration.
# """
# import random
# import string
# import os
# import logging
# from datetime import datetime, timedelta
# from typing import Dict, Optional

# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException

# from ..config import settings
# from ..utils.db import otp_collection

# # Configure logging
# logger = logging.getLogger(__name__)

# # Twilio configuration
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# # Initialize Twilio client if credentials are available
# twilio_client = None
# if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
#     twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# async def generate_otp(username: str) -> str:
#     """
#     Generate and store OTP for a user
#     """
#     # Generate random OTP
#     otp = ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))
    
#     # Calculate expiration time
#     expiry_time = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRATION_MINUTES)
    
#     # Store OTP in database
#     await otp_collection.update_one(
#         {"username": username},
#         {"$set": {
#             "otp": otp,
#             "expires_at": expiry_time
#         }},
#         upsert=True
#     )
    
#     logger.info(f"Generated OTP for user: {username}")
#     return otp

# async def verify_otp(username: str, otp: str) -> bool:
#     """
#     Verify OTP for a user
#     """
#     # Find OTP record in database
#     otp_record = await otp_collection.find_one({"username": username})
    
#     if not otp_record:
#         logger.warning(f"OTP record not found for user: {username}")
#         return False
        
#     # Check if OTP is expired
#     if datetime.utcnow() > otp_record["expires_at"]:
#         logger.warning(f"OTP expired for user: {username}")
#         return False
        
#     # Check if OTP matches
#     if otp_record["otp"] != otp:
#         logger.warning(f"Invalid OTP provided for user: {username}")
#         return False
        
#     # Delete OTP after successful verification
#     await otp_collection.delete_one({"username": username})
#     logger.info(f"OTP successfully verified for user: {username}")
    
#     return True

# async def send_otp_to_phone(phone_number: str, otp: str) -> bool:
#     """
#     Send OTP to a phone number using Twilio
#     """
#     if not twilio_client:
#         # Fallback if Twilio is not configured (for development)
#         logger.warning(f"Twilio not configured. Would send OTP {otp} to {phone_number}")
#         return True
    
#     try:
#         # Format phone number to international format if not already
#         if not phone_number.startswith('+'):
#             phone_number = f"+{phone_number}"
            
#         # Send SMS via Twilio
#         message = twilio_client.messages.create(
#             body=f"Your verification code is: {otp}. Valid for {settings.OTP_EXPIRATION_MINUTES} minutes.",
#             from_=TWILIO_PHONE_NUMBER,
#             to=phone_number
#         )
        
#         logger.info(f"OTP sent to {phone_number}, message SID: {message.sid}")
#         return True
        
#     except TwilioRestException as e:
#         logger.error(f"Twilio error: {str(e)}")
#         return False
#     except Exception as e:
#         logger.error(f"Error sending OTP: {str(e)}")
#         return False


"""
OTP generation, verification, and sending service with Twilio integration.
"""

# import random
# import string
# import logging
# from datetime import datetime, timedelta

# from typing import Optional

# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException

# from app.config import settings
# from app.utils.db import otp_collection

# # Configure logging
# logger = logging.getLogger(__name__)

# # Initialize Twilio client using settings
# twilio_client = None
# if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
#     twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
# else:
#     logger.warning("Twilio credentials not found. SMS sending will be skipped in development.")

# async def generate_otp(username: str) -> str:
#     """
#     Generate a numeric OTP and store it in the database for the given username.
#     """
#     otp = ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))
#     expiry_time = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRATION_MINUTES)

#     await otp_collection.update_one(
#         {"username": username},
#         {
#             "$set": {
#                 "otp": otp,
#                 "expires_at": expiry_time
#             }
#         },
#         upsert=True
#     )

#     logger.info(f"OTP generated for user: {username}")
#     return otp

# async def verify_otp(username: str, otp: str) -> bool:
#     """
#     Verify an OTP for the given username.
#     """
#     otp_record = await otp_collection.find_one({"username": username})
#     if not otp_record:
#         logger.warning(f"No OTP record found for user: {username}")
#         return False

#     if datetime.utcnow() > otp_record["expires_at"]:
#         logger.warning(f"OTP expired for user: {username}")
#         return False

#     if otp_record["otp"] != otp:
#         logger.warning(f"Incorrect OTP for user: {username}")
#         return False

#     await otp_collection.delete_one({"username": username})
#     logger.info(f"OTP successfully verified for user: {username}")
#     return True

# async def send_otp_to_phone(phone_number: str, otp: str) -> bool:
#     """
#     Send the OTP to the provided phone number using Twilio SMS.
#     """
#     if not twilio_client:
#         logger.info(f"Development mode: OTP {otp} would have been sent to {phone_number}")
#         return True  # Assume success in dev mode

#     try:
#         # Format phone number to international format
#         if not phone_number.startswith('+'):
#             phone_number = f"+{phone_number}"

#         message = twilio_client.messages.create(
#             body=f"Your verification code is: {otp}. It is valid for {settings.OTP_EXPIRATION_MINUTES} minutes.",
#             from_=settings.TWILIO_PHONE_NUMBER,
#             to=phone_number
#         )

#         logger.info(f"OTP sent to {phone_number}. Twilio SID: {message.sid}")
#         return True

#     except TwilioRestException as e:
#         logger.error(f"Twilio error: {e}")
#         return False
#     except Exception as e:
#         logger.error(f"Unexpected error while sending OTP: {e}")
#         return False

# import requests
# from requests.auth import HTTPBasicAuth
# from datetime import datetime, timedelta
# import random
# import string
# import os
# import logging
# import phonenumbers


# from twilio.base.exceptions import TwilioRestException

# from ..config import settings
# from ..utils.db import users_collection, otp_collection
# from ..utils.security import create_access_token
# from ..services.face_service import extract_face_embedding, verify_face

# # Configure logging
# logger = logging.getLogger(__name__)

# # Twilio configuration
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


# def is_valid_phone_number(phone_number: str) -> bool:
#     try:
#         parsed_number = phonenumbers.parse(phone_number, None)
#         return phonenumbers.is_valid_number(parsed_number)
#     except phonenumbers.NumberParseException:
#         return False

# def normalize_phone_number(phone_number: str, region: str = "IN") -> str:
#     try:
#         number = phonenumbers.parse(phone_number, region)
#         if not phonenumbers.is_valid_number(number):
#             return None
#         return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
#     except phonenumbers.NumberParseException:
#         return None

# async def create_user(username: str, phone_number: str):
#     phone_number = normalize_phone_number(phone_number, region="IN")
#     if not phone_number:
#         logger.warning(f"Invalid or unnormalizable phone number")
#         return None

#     existing_user = await users_collection.find_one({"username": username})
#     if existing_user:
#         return None

#     user = {
#         "username": username,
#         "phone_number": phone_number,
#         "is_active": True,
#         "is_admin": False,
#         "face_embedding": None,
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow()
#     }

#     result = await users_collection.insert_one(user)
#     user["_id"] = result.inserted_id
#     return user

# async def update_face_embedding(username: str, face_embedding: list) -> bool:
#     result = await users_collection.update_one(
#         {"username": username},
#         {"$set": {
#             "face_embedding": face_embedding,
#             "updated_at": datetime.utcnow()
#         }}
#     )
#     return result.modified_count > 0

# async def generate_otp(username: str) -> str:
#     otp = ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))
#     expiry = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRATION_MINUTES)
#     await otp_collection.update_one(
#         {"username": username},
#         {"$set": {"otp": otp, "expires_at": expiry}},
#         upsert=True
#     )
#     logger.info(f"Generated OTP for {username}")
#     return otp

# async def verify_otp(username: str, otp: str) -> bool:
#     record = await otp_collection.find_one({"username": username})
#     if not record:
#         logger.warning(f"No OTP for {username}")
#         return False
#     if datetime.utcnow() > record["expires_at"]:
#         logger.warning(f"OTP expired for {username}")
#         return False
#     if record["otp"] != otp:
#         logger.warning(f"Invalid OTP for {username}")
#         return False
#     await otp_collection.delete_one({"username": username})
#     return True

# def send_sms_via_http(phone_number: str, otp: str) -> bool:
#     url = f'https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json'
#     data = {
#         'From': TWILIO_PHONE_NUMBER,
#         'To': phone_number,
#         'Body': f"Your OTP is {otp}. Valid for {settings.OTP_EXPIRATION_MINUTES} minutes."
#     }
#     auth = HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

#     try:
#         response = requests.post(url, data=data, auth=auth)
#         if response.status_code == 201:
#             logger.info(f"OTP sent to {phone_number} via HTTP")
#             return True
#         else:
#             logger.error(f"Failed to send OTP: {response.status_code}, {response.text}")
#             return False
#     except Exception as e:
#         logger.error(f"Exception sending OTP: {e}")
#         return False

# async def send_otp_to_phone(phone_number: str, otp: str) -> bool:
#     if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER):
#         logger.warning(f"Twilio not configured. Would send OTP {otp} to {phone_number}")
#         return True
#     if not phone_number.startswith("+"):
#         phone_number = "+" + phone_number
#     return send_sms_via_http(phone_number, otp)

# async def request_otp_login(username: str):
#     user = await users_collection.find_one({"username": username})
#     if not user:
#         return False, "User not found"
#     otp = await generate_otp(username)
#     sent = await send_otp_to_phone(user["phone_number"], otp)
#     if not sent:
#         return False, "Failed to send OTP"
#     return True, "OTP sent successfully"

# async def verify_otp_login(username: str, otp: str):
#     user = await users_collection.find_one({"username": username})
#     if not user:
#         return False, None
#     is_valid = await verify_otp(username, otp)
#     if not is_valid:
#         return False, None
#     token = create_access_token({
#         "sub": user["username"],
#         "id": str(user["_id"]),
#         "is_admin": user.get("is_admin", False)
#     })
#     return True, {"access_token": token, "token_type": "bearer"}

# async def face_login(username: str, face_image: bytes):
#     user = await users_collection.find_one({"username": username})
#     if not user or not user.get("face_embedding"):
#         return False, None
#     new_embedding = extract_face_embedding(face_image)
#     if not new_embedding:
#         return False, None
#     if not verify_face(user["face_embedding"], new_embedding):
#         return False, None
#     token = create_access_token({
#         "sub": user["username"],
#         "id": str(user["_id"]),
#         "is_admin": user.get("is_admin", False)
#     })
#     return True, {"access_token": token, "token_type": "bearer"}

# import requests
# from datetime import datetime, timedelta
# import random
# import string
# import os
# import logging
# import phonenumbers 
# import asyncio

# from ..config import settings
# from ..utils.db import users_collection, otp_collection
# from ..utils.security import create_access_token
# from ..services.face_service import extract_face_embedding, verify_face

# # Configure logging
# logger = logging.getLogger(__name__)

# # Vonage (Nexmo) configuration
# VONAGE_API_KEY = os.getenv("VONAGE_API_KEY", "")  # Default to the provided API key
# VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET", "")  # Default to the provided API secret
# VONAGE_BRAND_NAME = os.getenv("VONAGE_BRAND_NAME", "")  # Default brand name


# def is_valid_phone_number(phone_number: str) -> bool:
#     try:
#         parsed_number = phonenumbers.parse(phone_number, None)
#         return phonenumbers.is_valid_number(parsed_number)
#     except phonenumbers.NumberParseException:
#         return False


# def normalize_phone_number(phone_number: str, region: str = "IN") -> str:
#     try:
#         number = phonenumbers.parse(phone_number, region)
#         if not phonenumbers.is_valid_number(number):
#             return None
#         # Return the number without the '+' prefix for Vonage API
#         formatted = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
#         return formatted
#     except phonenumbers.NumberParseException:
#         return None


# async def create_user(username: str, phone_number: str):
#     phone_number = normalize_phone_number(phone_number, region="IN")
#     if not phone_number:
#         logger.warning(f"Invalid or unnormalizable phone number")
#         return None

#     existing_user = await users_collection.find_one({"username": username})
#     if existing_user:
#         return None

#     user = {
#         "username": username,
#         "phone_number": phone_number,
#         "is_active": True,
#         "is_admin": False,
#         "face_embedding": None,
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow()
#     }

#     result = await users_collection.insert_one(user)
#     user["_id"] = result.inserted_id
#     return user


# async def update_face_embedding(username: str, face_embedding: list) -> bool:
#     result = await users_collection.update_one(
#         {"username": username},
#         {"$set": {
#             "face_embedding": face_embedding,
#             "updated_at": datetime.utcnow()
#         }}
#     )
#     return result.modified_count > 0


# async def generate_otp(username: str) -> str:
#     otp = ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))
#     expiry = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRATION_MINUTES)
#     await otp_collection.update_one(
#         {"username": username},
#         {"$set": {"otp": otp, "expires_at": expiry}},
#         upsert=True
#     )
#     logger.info(f"Generated OTP for {username}")
#     return otp

# # async def generate_otp(username: str) -> str:
# #     if not username:
# #         logger.error("Cannot generate OTP: username is empty or None")
# #         return None

# #     otp = ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))
# #     expiry = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRATION_MINUTES)

# #     result = await otp_collection.update_one(
# #         {"username": username},
# #         {"$set": {"otp": otp, "expires_at": expiry}},
# #         upsert=True
# #     )

# #     if result.upserted_id or result.modified_count:
# #         logger.info(f"OTP saved for {username}")
# #     else:
# #         logger.warning(f"OTP not saved or updated for {username}")

# #     return otp



# async def verify_otp(username: str, otp: str) -> bool:
#     record = await otp_collection.find_one({"username": username})
#     print(record)
#     if not record:
#         logger.warning(f"No OTP for {username}")
#         return False
#     if datetime.utcnow() > record["expires_at"]:
#         logger.warning(f"OTP expired for {username}")
#         return False
#     if record["otp"] != otp:
#         logger.warning(f"Invalid OTP for {username}")
#         return False
#    # await otp_collection.delete_one({"username": username})
#     return True


# def send_sms_via_http(phone_number: str, otp: str) -> bool:
#     url = 'https://rest.nexmo.com/sms/json'
    
#     # Make sure the phone number is in the correct format (without '+' prefix)
#     if phone_number.startswith('+'):
#         phone_number = phone_number[1:]  # Remove '+' prefix
    
#     data = {
#         'from': VONAGE_BRAND_NAME,
#         'text': f"Your OTP is {otp}. Valid for {settings.OTP_EXPIRATION_MINUTES} minutes.",
#         'to': phone_number,
#         'api_key': VONAGE_API_KEY,
#         'api_secret': VONAGE_API_SECRET
#     }

#     try:
#         response = requests.post(url, data=data)
#         response_data = response.json()
        
#         if response.status_code == 200 and response_data.get('messages') and response_data['messages'][0].get('status') == '0':
#             logger.info(f"OTP sent to {phone_number} via Vonage SMS API")
#             return True
#         else:
#             error_msg = response_data.get('messages', [{}])[0].get('error-text', 'Unknown error')
#             logger.error(f"Failed to send OTP: {response.status_code}, {error_msg}")
#             return False
#     except Exception as e:
#         logger.error(f"Exception sending OTP via Vonage: {e}")
#         return False




# async def send_otp_to_phone(phone_number: str, otp: str) -> bool:
#     if not (VONAGE_API_KEY and VONAGE_API_SECRET):
#         logger.warning(f"Vonage not configured. Would send OTP {otp} to {phone_number}")
#         return True
    
#     # Run the blocking HTTP call in a background thread
#     return await asyncio.to_thread(send_sms_via_http, phone_number, otp)



# async def request_otp_login(username: str):
#     user = await users_collection.find_one({"username": username})
#     if not user:
#         return False, "User not found"
#     otp = await generate_otp(username)
#     sent = await send_otp_to_phone(user["phone_number"], otp)
#     if not sent:
#         return False, "Failed to send OTP"
#     return True, "OTP sent successfully"


# async def verify_otp_login(username: str, otp: str):
#     user = await users_collection.find_one({"username": username})
#     if not user:
#         return False, None
#     is_valid = await verify_otp(username, otp)
#     if not is_valid:
#         return False, None
#     token = create_access_token({
#         "sub": user["username"],
#         "id": str(user["_id"]),
#         "is_admin": user.get("is_admin", False)
#     })
#     return True, {"access_token": token, "token_type": "bearer"}


# async def face_login(username: str, face_image: bytes):
#     user = await users_collection.find_one({"username": username})
#     if not user or not user.get("face_embedding"):
#         return False, None
#     new_embedding = extract_face_embedding(face_image)
#     if not new_embedding:
#         return False, None
#     if not verify_face(user["face_embedding"], new_embedding):
#         return False, None
#     token = create_access_token({
#         "sub": user["username"],
#         "id": str(user["_id"]),
#         "is_admin": user.get("is_admin", False)
#     })
#     return True, {"access_token": token, "token_type": "bearer"}
    
# if __name__ == "__main__":
#     generate_otp("garvi")




# auth_service.py (merged)

import requests
from datetime import datetime, timedelta
import random
import string
import os
import logging
import phonenumbers
import asyncio

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
from collections.abc import Sized

from ..config import settings
from ..utils.db import users_collection, otp_collection
from ..utils.security import create_access_token  # Optional if you already moved it here
from ..models.user import TokenData
from ..services.face_service import extract_face_embedding, verify_face

# Logging setup
logger = logging.getLogger(__name__)

# Vonage SMS config
VONAGE_API_KEY = os.getenv("VONAGE_API_KEY", "")
VONAGE_API_SECRET = os.getenv("VONAGE_API_SECRET", "")
VONAGE_BRAND_NAME = os.getenv("VONAGE_BRAND_NAME", "")

# OAuth2 token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# --- 🔐 JWT-related functions ---

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_user_by_username(username: str):
    return await users_collection.find_one({"username": username})

async def get_user_by_embedding(username: str):
    return await users_collection.find_one({"username": username})

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        user = await get_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_active_user(user: dict = Depends(get_current_user)):
    if not user["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

# --- 📱 Phone Utilities ---

def is_valid_phone_number(phone_number: str) -> bool:
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False

def normalize_phone_number(phone_number: str, region: str = "IN") -> str:
    try:
        number = phonenumbers.parse(phone_number, region)
        if not phonenumbers.is_valid_number(number):
            return None
        return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        return None

# --- 👤 User Registration ---

# async def create_user(username: str, phone_number: str):
#     phone_number = normalize_phone_number(phone_number)
#     if not phone_number:
#         logger.warning("Invalid phone number")
#         return None

#     existing_user = await users_collection.find_one({"username": username})
#     if existing_user:
#         return None

#     user = {
#         "username": username,
#         "phone_number": phone_number,
#         "is_active": True,
#         "is_admin": False,
#         "face_embedding": None,
#         "created_at": datetime.utcnow(),
#         "updated_at": datetime.utcnow()
#     }

#     result = await users_collection.insert_one(user)
#     user["_id"] = result.inserted_id
#     return user

async def create_user(username: str, phone_number: Optional[str] = None, face_embedding: Optional[list] = None):
    # if not phone_number and not face_embedding:
    #     logger.warning("Either phone number or face embedding must be provided.")
    #     return None
    # from collections.abc import Sized

    if (phone_number is None or not isinstance(phone_number, Sized) or len(phone_number) == 0) and (face_embedding is None or not isinstance(face_embedding, Sized) or len(face_embedding) == 0):
        logger.warning("Either phone number or face embedding must be provided.")
        return None


    if isinstance(phone_number, str) and phone_number.strip():
        phone_number = normalize_phone_number(phone_number)
        if not phone_number:
            logger.warning("Invalid phone number")
            return None
    else:
        phone_number = None  # Clean up in case it was a bad type

    existing_user = await users_collection.find_one({"username": username})
    if existing_user:
        logger.warning(f"User '{username}' already exists.")
        return None

    user = {
        "username": username,
        "phone_number": phone_number,
        "is_active": True,
        "is_admin": False,
        "face_embedding": face_embedding,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = await users_collection.insert_one(user)
    user["_id"] = result.inserted_id
    return user


# --- 🧠 Face Embedding Update ---

async def update_face_embedding(username: str, face_embedding: list) -> bool:
    result = await users_collection.update_one(
        {"username": username},
        {"$set": {"face_embedding": face_embedding, "updated_at": datetime.utcnow()}}
    )
    return result.modified_count > 0

# --- 🔢 OTP Logic ---

async def generate_otp(username: str) -> str:
    otp = ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))
    expiry = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRATION_MINUTES)
    await otp_collection.update_one(
        {"username": username},
        {"$set": {"otp": otp, "expires_at": expiry}},
        upsert=True
    )
    logger.info(f"Generated OTP for {username}")
    return otp

async def verify_otp(username: str, otp: str) -> bool:
    record = await otp_collection.find_one({"username": username})
    if not record or datetime.utcnow() > record["expires_at"] or record["otp"] != otp:
        logger.warning(f"OTP validation failed for {username}")
        return False
    return True

# --- ✉️ SMS Sending ---

def send_sms_via_http(phone_number: str, otp: str) -> bool:
    url = 'https://rest.nexmo.com/sms/json'
    phone_number = phone_number.lstrip('+')
    data = {
        'from': VONAGE_BRAND_NAME,
        'text': f"Your OTP is {otp}. Valid for {settings.OTP_EXPIRATION_MINUTES} minutes.",
        'to': phone_number,
        'api_key': VONAGE_API_KEY,
        'api_secret': VONAGE_API_SECRET
    }
    try:
        response = requests.post(url, data=data)
        response_data = response.json()
        if response.status_code == 200 and response_data.get('messages', [{}])[0].get('status') == '0':
            logger.info(f"OTP sent to {phone_number}")
            return True
        logger.error(f"Vonage error: {response_data}")
        return False
    except Exception as e:
        logger.error(f"SMS send failed: {e}")
        return False

async def send_otp_to_phone(phone_number: str, otp: str) -> bool:
    if not (VONAGE_API_KEY and VONAGE_API_SECRET):
        logger.warning(f"Vonage not configured; would send OTP {otp} to {phone_number}")
        return True
    return await asyncio.to_thread(send_sms_via_http, phone_number, otp)

# --- 🔑 Login Workflows ---

async def request_otp_login(username: str):
    user = await users_collection.find_one({"username": username})
    if not user:
        return False, "User not found"
    otp = await generate_otp(username)
    sent = await send_otp_to_phone(user["phone_number"], otp)
    return (sent, "OTP sent" if sent else "Failed to send OTP")

async def verify_otp_login(username: str, otp: str):
    user = await users_collection.find_one({"username": username})
    if not user or not await verify_otp(username, otp):
        return False, None
    token = create_access_token({
        "sub": user["username"],
        "id": str(user["_id"]),
        "is_admin": user.get("is_admin", False)
    })
    return True, {"access_token": token, "token_type": "bearer"}

async def face_login(username: str, face_image: bytes):
    user = await users_collection.find_one({"username": username})
    if not user or not user.get("face_embedding"):
        return False, None
    new_embedding = extract_face_embedding(face_image)
    if not new_embedding or not verify_face(user["face_embedding"], new_embedding):
        return False, None
    token = create_access_token({
        "sub": user["username"],
        "id": str(user["_id"]),
        "is_admin": user.get("is_admin", False)
    })
    return True, {"access_token": token, "token_type": "bearer"}
