from pydantic import BaseModel
from typing import Optional


class STTUploadRequest(BaseModel):
    file_name: str
    content_type: str
    duration: Optional[float] = None
    language: Optional[str] = None


class STTUploadResponse(BaseModel):
    stt_id: str
    upload_url: str
    status: str


class STTStatusResponse(BaseModel):
    stt_id: str
    status: str
    progress: Optional[float] = None
    updated_at: Optional[str] = None


class STTTextResponse(BaseModel):
    stt_id: str
    text: str
    duration: Optional[float] = None
    language: Optional[str] = None
    created_at: str


class STTSummaryResponse(BaseModel):
    summary: str
    keywords: Optional[list] = None
    generated_at: str


class STTShareRequest(BaseModel):
    target_user_id: str
    include_summary: Optional[bool] = None


class MessageResponse(BaseModel):
    message: str
    shared_at: Optional[str] = None
