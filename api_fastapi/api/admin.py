from fastapi import APIRouter, Depends, HTTPException
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.admin import (
    AdminCreateUserRequest,
    AdminUserSummary,
    AdminUserListResponse,
    AdminUpdateUserRequest,
    MessageResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(user):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="권한 없음")


@router.post("/users", response_model=AdminUserSummary, status_code=201)
async def create_user(payload: AdminCreateUserRequest, user=Depends(get_current_user)) -> AdminUserSummary:
    require_admin(user)
    if any(u for u in db.users.values() if u["email"] == payload.email):
        raise HTTPException(status_code=409, detail="중복된 이메일")
    user_id = db.next_id("user")
    now = db.now()
    db.users[user_id] = {
        "id": user_id,
        "email": payload.email,
        "password": payload.password,
        "name": payload.name,
        "role": payload.role or "user",
        "created_at": now,
        "active": True,
    }
    return AdminUserSummary(id=user_id, email=payload.email, role=payload.role or "user", created_at=now, name=payload.name, active=True)


@router.get("/users", response_model=AdminUserListResponse)
async def list_users(q: str | None = None, role: str | None = None, page: int = 1, size: int = 20, user=Depends(get_current_user)) -> AdminUserListResponse:
    require_admin(user)
    items = list(db.users.values())
    if q:
        items = [u for u in items if q.lower() in u.get("email", "").lower() or q.lower() in (u.get("name") or "").lower()]
    if role:
        items = [u for u in items if u.get("role") == role]
    start = (page - 1) * size
    end = start + size
    sliced = items[start:end]
    summaries = [AdminUserSummary(id=u["id"], email=u["email"], role=u["role"], created_at=u["created_at"], name=u.get("name"), active=u.get("active", True)) for u in sliced]
    return AdminUserListResponse(users=summaries, pagination={"page": page, "total": len(items)})


@router.get("/users/{user_id}", response_model=AdminUserSummary)
async def get_user(user_id: str, user=Depends(get_current_user)) -> AdminUserSummary:
    require_admin(user)
    target = db.users.get(user_id)
    if not target:
        raise HTTPException(status_code=404, detail="사용자 없음")
    return AdminUserSummary(id=target["id"], email=target["email"], role=target["role"], created_at=target["created_at"], name=target.get("name"), active=target.get("active", True))


@router.patch("/users/{user_id}", response_model=MessageResponse)
async def update_user(user_id: str, payload: AdminUpdateUserRequest, user=Depends(get_current_user)) -> MessageResponse:
    require_admin(user)
    target = db.users.get(user_id)
    if not target:
        raise HTTPException(status_code=404, detail="대상 없음")
    if payload.role:
        target["role"] = payload.role
    if payload.active is not None:
        target["active"] = payload.active
    db.users[user_id] = target
    return MessageResponse(message="사용자 정보가 변경되었습니다")
