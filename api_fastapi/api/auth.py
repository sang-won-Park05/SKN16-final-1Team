from fastapi import APIRouter, HTTPException, status
from api_fastapi.schemas.auth import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    PasswordResetConfirm,
    SessionResponse,
    MessageResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/auth", tags=["auth"])


def normalize_email(email: str) -> str:
    return email.strip().lower()


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupRequest) -> SignupResponse:
    email = normalize_email(payload.email)
    if any(u for u in db.users.values() if u["email"] == email):
        raise HTTPException(status_code=409, detail="이미 존재하는 이메일")
    user_id = db.next_id("user")
    now = db.now()
    user = {
        "id": user_id,
        "email": email,
        "password": payload.password,
        "name": payload.name,
        "role": "user",
        "created_at": now,
        "active": True,
    }
    db.create_user(user)
    tokens = db.issue_tokens(user_id)
    return SignupResponse(
        id=user_id,
        email=email,
        name=payload.name,
        role="user",
        created_at=now,
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    email = normalize_email(payload.email)
    user = next((u for u in db.users.values() if u["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 이메일")
    if user.get("password") != payload.password:
        raise HTTPException(status_code=401, detail="잘못된 자격 증명")
    tokens = db.issue_tokens(user["id"])
    return TokenResponse(
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type="Bearer",
        expires_in=3600,
    )


@router.post("/token/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest) -> TokenResponse:
    user_id = db.refresh_tokens.get(payload.refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰")
    tokens = db.issue_tokens(user_id)
    return TokenResponse(access_token=tokens["access_token"], expires_in=3600)


@router.post("/logout", response_model=MessageResponse)
async def logout(access_token: str | None = None) -> MessageResponse:
    if access_token and access_token in db.tokens:
        db.tokens.pop(access_token, None)
    return MessageResponse(message="로그아웃되었습니다")


@router.get("/session", response_model=SessionResponse)
async def session(authorization: str | None = None) -> SessionResponse:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="인증 필요")
    token = authorization.split(" ", 1)[1]
    user_id = db.tokens.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰")
    user = db.users[user_id]
    return SessionResponse(**{k: user[k] for k in ["id", "email", "name", "role", "created_at"]})


@router.post("/password/reset-confirm", response_model=MessageResponse)
async def reset_confirm(payload: PasswordResetConfirm) -> MessageResponse:
    if payload.password_confirm and payload.new_password != payload.password_confirm:
        raise HTTPException(status_code=400, detail="비밀번호 불일치")
    return MessageResponse(message="비밀번호가 변경되었습니다")
