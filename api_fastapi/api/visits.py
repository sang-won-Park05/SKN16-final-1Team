from fastapi import APIRouter, Depends, HTTPException, Query
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.visits import (
    VisitCreate,
    Visit,
    VisitListResponse,
    VisitUpdate,
    PrescriptionCreate,
    MessageResponse,
    JobResponse,
    TextResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/visits", tags=["visits"])


@router.post("/", response_model=Visit, status_code=201)
async def create_visit(payload: VisitCreate, user=Depends(get_current_user)) -> Visit:
    visit_id = db.next_id("visit")
    record = payload.model_dump(exclude_none=True)
    record.update({"id": visit_id, "created_at": db.now()})
    db.visits[visit_id] = record
    return Visit(**record)


@router.get("/", response_model=VisitListResponse)
async def list_visits(
    from_: str | None = Query(default=None, alias="from"),
    to: str | None = None,
    dept: str | None = None,
    hospital: str | None = None,
    q: str | None = None,
    page: int = 1,
    size: int = 10,
    order: str = "desc",
    user=Depends(get_current_user),
) -> VisitListResponse:
    items = list(db.visits.values())
    if dept:
        items = [v for v in items if v.get("dept") == dept]
    if hospital:
        items = [v for v in items if v.get("hospital") == hospital]
    if q:
        items = [v for v in items if q.lower() in v.get("memo", "").lower()]
    items = sorted(items, key=lambda v: v.get("date", ""), reverse=(order == "desc"))
    start = (page - 1) * size
    end = start + size
    sliced = items[start:end]
    return VisitListResponse(visits=[Visit(**v) for v in sliced], pagination={"page": page, "total": len(items)})


@router.get("/{visit_id}", response_model=Visit)
async def get_visit(visit_id: str, user=Depends(get_current_user)) -> Visit:
    visit = db.visits.get(visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="기록 없음")
    return Visit(**visit)


@router.patch("/{visit_id}", response_model=MessageResponse)
async def update_visit(visit_id: str, payload: VisitUpdate, user=Depends(get_current_user)) -> MessageResponse:
    visit = db.visits.get(visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="기록 없음")
    visit.update(payload.model_dump(exclude_none=True))
    db.visits[visit_id] = visit
    return MessageResponse(message="진료 기록이 수정되었습니다")


@router.delete("/{visit_id}", response_model=MessageResponse)
async def delete_visit(visit_id: str, user=Depends(get_current_user)) -> MessageResponse:
    db.visits.pop(visit_id, None)
    return MessageResponse(message="진료기록이 삭제되었습니다")


@router.post("/{visit_id}/presc", response_model=MessageResponse)
async def add_prescription(visit_id: str, payload: PrescriptionCreate, user=Depends(get_current_user)) -> MessageResponse:
    if visit_id not in db.visits:
        raise HTTPException(status_code=404, detail="기록 없음")
    presc_id = db.next_id("presc")
    prescs = db.prescriptions.setdefault(visit_id, [])
    prescs.append({"id": presc_id, **payload.model_dump(exclude_none=True)})
    return MessageResponse(message="처방이 추가되었습니다")


@router.get("/{visit_id}/presc", response_model=dict)
async def list_prescriptions(visit_id: str, user=Depends(get_current_user)) -> dict:
    return {"presc": db.prescriptions.get(visit_id, [])}


@router.patch("/{visit_id}/presc/{presc_id}", response_model=MessageResponse)
async def update_prescription(visit_id: str, presc_id: str, payload: PrescriptionCreate, user=Depends(get_current_user)) -> MessageResponse:
    prescs = db.prescriptions.get(visit_id, [])
    target = next((p for p in prescs if p["id"] == presc_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="대상 없음")
    target.update(payload.model_dump(exclude_none=True))
    return MessageResponse(message="처방이 수정되었습니다")


@router.delete("/{visit_id}/presc/{presc_id}", response_model=MessageResponse)
async def delete_prescription(visit_id: str, presc_id: str, user=Depends(get_current_user)) -> MessageResponse:
    prescs = db.prescriptions.get(visit_id, [])
    db.prescriptions[visit_id] = [p for p in prescs if p["id"] != presc_id]
    return MessageResponse(message="처방이 삭제되었습니다")


@router.post("/{visit_id}/stt", response_model=JobResponse)
async def upload_visit_stt(visit_id: str, user=Depends(get_current_user)) -> JobResponse:
    job_id = db.next_id("stt")
    db.stt_jobs[job_id] = {"visit_id": visit_id, "status": "pending", "text": None}
    return JobResponse(job_id=job_id, status="pending")


@router.get("/{visit_id}/stt/status", response_model=JobResponse)
async def stt_status(visit_id: str, user=Depends(get_current_user)) -> JobResponse:
    pair = next(((jid, j) for jid, j in db.stt_jobs.items() if j.get("visit_id") == visit_id), None)
    if not pair:
        raise HTTPException(status_code=404, detail="기록 없음")
    jid, job = pair
    return JobResponse(job_id=jid, status=job.get("status", "pending"))


@router.get("/{visit_id}/stt/text", response_model=TextResponse)
async def stt_text(visit_id: str, user=Depends(get_current_user)) -> TextResponse:
    job = next((j for jid, j in db.stt_jobs.items() if j.get("visit_id") == visit_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="기록 없음")
    return TextResponse(text=job.get("text") or "변환된 텍스트 예시")


@router.post("/{visit_id}/ocr", response_model=JobResponse)
async def request_ocr(visit_id: str, user=Depends(get_current_user)) -> JobResponse:
    job_id = db.next_id("ocr")
    db.file_ocr_jobs[job_id] = {"visit_id": visit_id, "status": "pending", "text": None}
    return JobResponse(job_id=job_id, status="pending")


@router.get("/{visit_id}/ocr/status", response_model=JobResponse)
async def ocr_status(visit_id: str, user=Depends(get_current_user)) -> JobResponse:
    pair = next(((jid, j) for jid, j in db.file_ocr_jobs.items() if j.get("visit_id") == visit_id), None)
    if not pair:
        raise HTTPException(status_code=404, detail="기록 없음")
    jid, job = pair
    return JobResponse(job_id=jid, status=job.get("status", "pending"))


@router.get("/{visit_id}/ocr/text", response_model=TextResponse)
async def ocr_text(visit_id: str, user=Depends(get_current_user)) -> TextResponse:
    job = next((j for jid, j in db.file_ocr_jobs.items() if j.get("visit_id") == visit_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="기록 없음")
    return TextResponse(text=job.get("text") or "OCR 분석 결과 예시")
