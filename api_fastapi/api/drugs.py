from fastapi import APIRouter, Depends, HTTPException
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.drugs import (
    MedCreate,
    Med,
    MedListResponse,
    MedUpdate,
    PillLookupRequest,
    PillLookupResponse,
    DrugInfoResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/drugs", tags=["drugs"])


@router.post("/meds", response_model=Med, status_code=201)
async def add_med(payload: MedCreate, user=Depends(get_current_user)) -> Med:
    med_id = db.next_id("drug")
    record = payload.model_dump(exclude_none=True)
    record.update({"id": med_id, "status": "active", "created_at": db.now()})
    db.drugs[med_id] = record
    return Med(**record)


@router.get("/meds", response_model=MedListResponse)
async def list_meds(q: str | None = None, type: str | None = None, status: str | None = None, user=Depends(get_current_user)) -> MedListResponse:
    items = list(db.drugs.values())
    if q:
        items = [m for m in items if q.lower() in m.get("name", "").lower()]
    if status:
        items = [m for m in items if m.get("status") == status]
    return MedListResponse(meds=[Med(**m) for m in items])


@router.get("/meds/{med_id}", response_model=Med)
async def get_med(med_id: str, user=Depends(get_current_user)) -> Med:
    med = db.drugs.get(med_id)
    if not med:
        raise HTTPException(status_code=404, detail="대상 없음")
    return Med(**med)


@router.patch("/meds/{med_id}", response_model=dict)
async def update_med(med_id: str, payload: MedUpdate, user=Depends(get_current_user)) -> dict:
    med = db.drugs.get(med_id)
    if not med:
        raise HTTPException(status_code=404, detail="대상 없음")
    med.update(payload.model_dump(exclude_none=True))
    db.drugs[med_id] = med
    return {"message": "복용약 정보가 수정되었습니다"}


@router.delete("/meds/{med_id}", response_model=dict)
async def delete_med(med_id: str, user=Depends(get_current_user)) -> dict:
    med = db.drugs.get(med_id)
    if not med:
        raise HTTPException(status_code=404, detail="대상 없음")
    med["status"] = "stopped"
    return {"message": "복용약이 중단되었습니다"}


@router.post("/pill-lookup", response_model=PillLookupResponse)
async def pill_lookup(payload: PillLookupRequest, user=Depends(get_current_user)) -> PillLookupResponse:
    return PillLookupResponse(
        name="타이레놀 500mg",
        ingredient="Acetaminophen",
        manufacturer="한국얀센",
        image_url="https://pillimg.com/ty500.jpg",
    )


@router.get("/info", response_model=DrugInfoResponse)
async def drug_info(name: str, ingredient: str | None = None, user=Depends(get_current_user)) -> DrugInfoResponse:
    return DrugInfoResponse(
        name=name,
        ingredient=ingredient or "Acetaminophen",
        efficacy="해열·진통 완화",
        caution="간질환 환자 주의",
        side_effects=["피로감", "오심"],
    )
