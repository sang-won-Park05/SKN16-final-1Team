from pydantic import BaseModel
from typing import Optional, List


class VisitCreate(BaseModel):
    hospital: str
    date: str
    dept: str
    diagnosis_code: str
    memo: Optional[str] = None
    file_ids: Optional[List[str]] = None


class Visit(BaseModel):
    id: str
    hospital: str
    date: str
    dept: str
    diagnosis_code: str
    memo: Optional[str] = None
    created_at: str


class VisitListResponse(BaseModel):
    visits: List[Visit]
    pagination: dict


class VisitUpdate(BaseModel):
    memo: Optional[str] = None
    dept: Optional[str] = None
    diagnosis_code: Optional[str] = None


class PrescriptionCreate(BaseModel):
    drug_name: str
    dosage: str
    period: int
    frequency: Optional[int] = None


class Prescription(BaseModel):
    id: str
    drug_name: str
    dosage: str
    period: int
    frequency: Optional[int] = None


class MessageResponse(BaseModel):
    message: str


class JobResponse(BaseModel):
    job_id: str
    status: str
    estimated_time: Optional[int] = None


class TextResponse(BaseModel):
    text: str
