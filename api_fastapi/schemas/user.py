from pydantic import BaseModel, EmailStr
from typing import Optional


class UserProfile(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str] = None
    role: str
    created_at: str


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class MessageResponse(BaseModel):
    message: str
