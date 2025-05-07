# from datetime import datetime
# from typing import List, Optional
# from pydantic import Field
# from pydantic_settings import BaseSettings, SettingsConfigDict
# from bson import ObjectId
# from pydantic.json_schema import JsonSchemaValue
# from pydantic import GetJsonSchemaHandler

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)

#     @classmethod
#     def __get_pydantic_json_schema__(cls, core_schema: dict, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
#         return {"type": "string"}

# class UserBase(BaseSettings):
#     username: str = Field(..., min_length=3, max_length=50)
#     phone_number: str = Field(..., min_length=10, max_length=15)
#     is_active: bool = True
#     is_admin: bool = False

#     model_config = SettingsConfigDict(validate_default=False)

# class UserCreate(UserBase):
#     pass

# class UserInDB(UserBase):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     face_embedding: Optional[List[float]] = None
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)

#     model_config = SettingsConfigDict(validate_default=False)

# class User(UserBase):
#     id: str = Field(...)
#     created_at: datetime
#     updated_at: datetime

#     model_config = SettingsConfigDict(validate_default=False)

# class OTPRequest(BaseSettings):
#     username: str

#     model_config = SettingsConfigDict(validate_default=False)

# class OTPVerify(BaseSettings):
#     username: str
#     otp_code: str

#     model_config = SettingsConfigDict(validate_default=False)

# class FaceLoginRequest(BaseSettings):
#     username: str

#     model_config = SettingsConfigDict(validate_default=False)

# class Token(BaseSettings):
#     access_token: str
#     token_type: str = "bearer"

#     model_config = SettingsConfigDict(validate_default=False)

# class TokenData(BaseSettings):
#     username: Optional[str] = None
#     user_id: Optional[str] = None
#     is_admin: bool = False

#     model_config = SettingsConfigDict(validate_default=False)

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic.json_schema import JsonSchemaValue
from bson import ObjectId
from pydantic import GetJsonSchemaHandler

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: dict, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {"type": "string"}

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15)
    is_active: bool = True
    is_admin: bool = False

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    face_embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }

class User(UserBase):
    id: str = Field(...)
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
    }

class OTPRequest(BaseModel):
    username: str

class OTPVerify(BaseModel):
    username: str
    otp_code: str

class FaceLoginRequest(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None
    is_admin: bool = False
