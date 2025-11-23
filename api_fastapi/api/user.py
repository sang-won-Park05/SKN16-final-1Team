from fastapi import APIRouter, Depends, HTTPException
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.user import UserProfile, UserUpdateRequest, MessageResponse
from api_fastapi.core.database import db

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserProfile)
async def me(user=Depends(get_current_user)) -> UserProfile:
    return UserProfile(**{k: user.get(k) for k in ["id", "email", "name", "role", "created_at"]})


@router.patch("/me", response_model=MessageResponse)
async def update_me(payload: UserUpdateRequest, user=Depends(get_current_user)) -> MessageResponse:
    if payload.email:
        if any(u for u in db.users.values() if u["email"] == payload.email and u["id"] != user["id"]):
            raise HTTPException(status_code=400, detail="형식 오류")
        user["email"] = payload.email
    if payload.name:
        user["name"] = payload.name
    if payload.password:
        user["password"] = payload.password
    db.users[user["id"]] = user
    return MessageResponse(message="정보가 수정되었습니다")


@router.delete("/me", response_model=MessageResponse)
async def delete_me(user=Depends(get_current_user)) -> MessageResponse:
    db.users.pop(user["id"], None)
    return MessageResponse(message="계정이 삭제되었습니다")
