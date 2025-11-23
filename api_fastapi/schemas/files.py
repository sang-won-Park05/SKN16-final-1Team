from pydantic import BaseModel
from typing import Optional


class FileUploadRequest(BaseModel):
    file_name: str
    content_type: str
    size: Optional[int] = None


class FileUploadResponse(BaseModel):
    upload_url: str
    file_id: str


class FileMeta(BaseModel):
    id: str
    file_name: str
    size: Optional[int] = None
    uploaded_by: str
    created_at: str


class OCRJobResponse(BaseModel):
    job_id: str
    status: str


class OCRTextResponse(BaseModel):
    text: str


class MessageResponse(BaseModel):
    message: str
