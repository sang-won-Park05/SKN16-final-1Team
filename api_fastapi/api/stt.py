from fastapi import APIRouter, Depends, HTTPException
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.stt import (
    STTUploadRequest,
    STTUploadResponse,
    STTStatusResponse,
    STTTextResponse,
    STTSummaryResponse,
    STTShareRequest,
    MessageResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/stt", tags=["stt"])


@router.post("/upload", response_model=STTUploadResponse, status_code=201)
async def upload(payload: STTUploadRequest, user=Depends(get_current_user)) -> STTUploadResponse:
    stt_id = db.next_id("stt")
    db.stt_jobs[stt_id] = {
        "id": stt_id,
        "file_name": payload.file_name,
        "status": "pending",
        "text": None,
        "created_at": db.now(),
        "duration": payload.duration,
        "language": payload.language,
    }
    return STTUploadResponse(stt_id=stt_id, upload_url=f"https://s3.aws.com/stt/{stt_id}", status="pending")


@router.get("/{stt_id}/status", response_model=STTStatusResponse)
async def status(stt_id: str, user=Depends(get_current_user)) -> STTStatusResponse:
    job = db.stt_jobs.get(stt_id)
    if not job:
        raise HTTPException(status_code=404, detail="대상 없음")
    return STTStatusResponse(stt_id=stt_id, status=job.get("status", "pending"), progress=job.get("progress"), updated_at=db.now())


@router.get("/{stt_id}/text", response_model=STTTextResponse)
async def text(stt_id: str, user=Depends(get_current_user)) -> STTTextResponse:
    job = db.stt_jobs.get(stt_id)
    if not job:
        raise HTTPException(status_code=404, detail="대상 없음")
    return STTTextResponse(stt_id=stt_id, text=job.get("text") or "변환된 텍스트", duration=job.get("duration"), language=job.get("language"), created_at=job.get("created_at", db.now()))


@router.get("/{stt_id}/summary", response_model=STTSummaryResponse)
async def summary(stt_id: str, user=Depends(get_current_user)) -> STTSummaryResponse:
    job = db.stt_jobs.get(stt_id)
    if not job:
        raise HTTPException(status_code=404, detail="대상 없음")
    return STTSummaryResponse(summary="환자 복통 호소, 소화불량 진단 및 약 처방", keywords=["복통", "소화불량", "약 처방"], generated_at=db.now())


@router.post("/{stt_id}/share", response_model=MessageResponse)
async def share(stt_id: str, payload: STTShareRequest, user=Depends(get_current_user)) -> MessageResponse:
    if stt_id not in db.stt_jobs:
        raise HTTPException(status_code=404, detail="대상 없음")
    return MessageResponse(message="STT 결과가 공유되었습니다", shared_at=db.now())
