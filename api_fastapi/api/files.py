from fastapi import APIRouter, Depends, HTTPException
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.files import (
    FileUploadRequest,
    FileUploadResponse,
    FileMeta,
    OCRJobResponse,
    OCRTextResponse,
    MessageResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", response_model=FileUploadResponse, status_code=201)
async def upload(payload: FileUploadRequest, user=Depends(get_current_user)) -> FileUploadResponse:
    file_id = db.next_id("file")
    db.files[file_id] = {
        "id": file_id,
        "file_name": payload.file_name,
        "size": payload.size,
        "content_type": payload.content_type,
        "uploaded_by": user["id"],
        "created_at": db.now(),
    }
    return FileUploadResponse(upload_url=f"https://s3.aws.com/upload/{file_id}", file_id=file_id)


@router.get("/{file_id}", response_model=FileMeta)
async def metadata(file_id: str, user=Depends(get_current_user)) -> FileMeta:
    meta = db.files.get(file_id)
    if not meta:
        raise HTTPException(status_code=404, detail="파일 없음")
    return FileMeta(**meta)


@router.post("/{file_id}/ocr", response_model=OCRJobResponse)
async def start_ocr(file_id: str, user=Depends(get_current_user)) -> OCRJobResponse:
    job_id = db.next_id("ocr")
    db.file_ocr_jobs[job_id] = {"file_id": file_id, "status": "pending", "text": None}
    return OCRJobResponse(job_id=job_id, status="pending")


@router.get("/{file_id}/ocr/status", response_model=OCRJobResponse)
async def ocr_status(file_id: str, user=Depends(get_current_user)) -> OCRJobResponse:
    job = next((j for j in db.file_ocr_jobs.values() if j.get("file_id") == file_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="대상 없음")
    return OCRJobResponse(job_id=job.get("id", ""), status=job.get("status", "pending"))


@router.get("/{file_id}/ocr/text", response_model=OCRTextResponse)
async def ocr_text(file_id: str, user=Depends(get_current_user)) -> OCRTextResponse:
    job = next((j for j in db.file_ocr_jobs.values() if j.get("file_id") == file_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="대상 없음")
    return OCRTextResponse(text=job.get("text") or "진료비 영수증: 총액 30,000원...")


@router.delete("/{file_id}", response_model=MessageResponse)
async def delete_file(file_id: str, user=Depends(get_current_user)) -> MessageResponse:
    db.files.pop(file_id, None)
    return MessageResponse(message="파일이 삭제되었습니다")
