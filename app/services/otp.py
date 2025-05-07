"""
OTP generation and verification service.
"""
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional

from ..config import settings
from ..utils.db import otp_collection

async def generate_otp(username: str) -> str:
    """
    Generate and store OTP for a user
    """
    # Generate random OTP
    otp = ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))
    
    # Calculate expiration time
    expiry_time = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRATION_MINUTES)
    
    # Store OTP in database
    await otp_collection.update_one(
        {"username": username},
        {"$set": {
            "otp": otp,
            "expires_at": expiry_time
        }},
        upsert=True
    )
    
    return otp

async def verify_otp(username: str, otp: str) -> bool:
    """
    Verify OTP for a user
    """
    # Find OTP record in database
    otp_record = await otp_collection.find_one({"username": username})
    
    if not otp_record:
        return False
        
    # Check if OTP is expired
    if datetime.utcnow() > otp_record["expires_at"]:
        return False
        
    # Check if OTP matches
    if otp_record["otp"] != otp:
        return False
        
    # Delete OTP after successful verification
    await otp_collection.delete_one({"username": username})
    
    return True

async def send_otp_to_phone(phone_number: str, otp: str) -> bool:
    """
    Send OTP to a phone number
    In a real application, this would integrate with an SMS service like Twilio
    
    For this example, we'll just simulate sending and return True
    """
    # In a real application, use an SMS service API here
    print(f"Sending OTP {otp} to {phone_number}")
    
    # For demo purposes, always return success
    return True