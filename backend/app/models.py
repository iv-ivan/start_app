from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    passwordHash: bytes


class UserInput(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
