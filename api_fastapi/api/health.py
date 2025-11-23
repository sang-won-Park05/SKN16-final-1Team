from fastapi import APIRouter, Depends, HTTPException
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.health import (
    HealthProfile,
    HealthHistoryItem,
    ConditionCreate,
    Condition,
    AllergyCreate,
    Allergy,
    MessageResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/profile", response_model=HealthProfile)
async def get_profile(user=Depends(get_current_user)) -> HealthProfile:
    return HealthProfile(**db.health_profiles.get(user["id"], {}))


@router.post("/profile", response_model=MessageResponse, status_code=201)
async def create_profile(payload: HealthProfile, user=Depends(get_current_user)) -> MessageResponse:
    db.health_profiles[user["id"]] = payload.model_dump(exclude_none=True)
    db.health_history[user["id"]] = [
        {"version": 1, "changes": payload.model_dump(exclude_none=True), "changed_at": db.now()}
    ]
    return MessageResponse(message="건강 프로필이 등록되었습니다")


@router.patch("/profile", response_model=MessageResponse)
async def update_profile(payload: HealthProfile, user=Depends(get_current_user)) -> MessageResponse:
    current = db.health_profiles.get(user["id"], {})
    changes = payload.model_dump(exclude_none=True)
    current.update(changes)
    db.health_profiles[user["id"]] = current
    history = db.health_history.setdefault(user["id"], [])
    history.append({"version": len(history) + 1, "changes": changes, "changed_at": db.now()})
    return MessageResponse(message="프로필이 수정되었습니다")


@router.get("/profile/history", response_model=list[HealthHistoryItem])
async def profile_history(user=Depends(get_current_user)) -> list[HealthHistoryItem]:
    return [HealthHistoryItem(**h) for h in db.health_history.get(user["id"], [])]


@router.post("/conditions", response_model=Condition, status_code=201)
async def add_condition(payload: ConditionCreate, user=Depends(get_current_user)) -> Condition:
    cond_id = db.next_id("cond")
    record = payload.model_dump(exclude_none=True)
    record.update({"id": cond_id, "status": record.get("status", "active"), "created_at": db.now()})
    db.conditions[cond_id] = record
    return Condition(**record)


@router.get("/conditions", response_model=dict)
async def list_conditions(status: str | None = None, user=Depends(get_current_user)) -> dict:
    items = list(db.conditions.values())
    if status:
        items = [c for c in items if c.get("status") == status]
    return {"conditions": items}


@router.get("/conditions/{cond_id}", response_model=Condition)
async def get_condition(cond_id: str, user=Depends(get_current_user)) -> Condition:
    cond = db.conditions.get(cond_id)
    if not cond:
        raise HTTPException(status_code=404, detail="대상 없음")
    return Condition(**cond)


@router.patch("/conditions/{cond_id}", response_model=MessageResponse)
async def update_condition(cond_id: str, payload: ConditionCreate, user=Depends(get_current_user)) -> MessageResponse:
    cond = db.conditions.get(cond_id)
    if not cond:
        raise HTTPException(status_code=404, detail="대상 없음")
    changes = payload.model_dump(exclude_none=True)
    cond.update(changes)
    cond["updated_at"] = db.now()
    db.conditions[cond_id] = cond
    return MessageResponse(message="질환 정보가 수정되었습니다(이력 생성)")


@router.delete("/conditions/{cond_id}", response_model=MessageResponse)
async def delete_condition(cond_id: str, user=Depends(get_current_user)) -> MessageResponse:
    db.conditions.pop(cond_id, None)
    return MessageResponse(message="질환이 삭제(또는 종료)되었습니다")


@router.post("/allergies", response_model=Allergy, status_code=201)
async def add_allergy(payload: AllergyCreate, user=Depends(get_current_user)) -> Allergy:
    alg_id = db.next_id("alg")
    record = payload.model_dump(exclude_none=True)
    record.update({"id": alg_id, "created_at": db.now()})
    db.allergies[alg_id] = record
    return Allergy(**record)


@router.get("/allergies", response_model=dict)
async def list_allergies(user=Depends(get_current_user)) -> dict:
    return {"allergies": list(db.allergies.values())}


@router.patch("/allergies/{alg_id}", response_model=MessageResponse)
async def update_allergy(alg_id: str, payload: AllergyCreate, user=Depends(get_current_user)) -> MessageResponse:
    alg = db.allergies.get(alg_id)
    if not alg:
        raise HTTPException(status_code=404, detail="대상 없음")
    alg.update(payload.model_dump(exclude_none=True))
    db.allergies[alg_id] = alg
    return MessageResponse(message="알러지 정보가 수정되었습니다")


@router.delete("/allergies/{alg_id}", response_model=MessageResponse)
async def delete_allergy(alg_id: str, user=Depends(get_current_user)) -> MessageResponse:
    db.allergies.pop(alg_id, None)
    return MessageResponse(message="알러지가 삭제되었습니다")
