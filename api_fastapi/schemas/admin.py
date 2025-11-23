from pydantic import BaseModel, EmailStr
from typing import Optional, List


class AdminCreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: Optional[str] = "user"


class AdminUserSummary(BaseModel):
    id: str
    email: EmailStr
    role: str
    created_at: str
    name: Optional[str] = None
    active: bool = True


class AdminUserListResponse(BaseModel):
    users: List[AdminUserSummary]
    pagination: dict


class AdminUpdateUserRequest(BaseModel):
    role: Optional[str] = None
    active: Optional[bool] = None


class MessageResponse(BaseModel):
    message: str
