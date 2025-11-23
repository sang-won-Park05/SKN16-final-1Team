from pydantic import BaseModel, EmailStr
from typing import Optional


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    auto_login: Optional[bool] = False


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None


class SignupResponse(TokenResponse):
    id: str
    email: EmailStr
    name: str
    role: str = "user"
    created_at: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    password_confirm: Optional[str] = None


class SessionResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: str
    created_at: str


class MessageResponse(BaseModel):
    message: str
