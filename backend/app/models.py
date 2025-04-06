from pydantic import BaseModel, EmailStr
import datetime
from bson.objectid import ObjectId


class User(BaseModel):
    email: EmailStr
    passwordHash: bytes


class Session(BaseModel):
    token: str
    userId: ObjectId
    expiresAt: datetime.datetime

    class Config:
        # Allowing ObjectId
        arbitrary_types_allowed = True


class UserInput(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
