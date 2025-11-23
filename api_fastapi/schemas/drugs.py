from pydantic import BaseModel
from typing import Optional, List


class MedCreate(BaseModel):
    name: str
    dosage: str
    frequency: int
    period: int
    start_date: Optional[str] = None
    memo: Optional[str] = None


class Med(BaseModel):
    id: str
    name: str
    dosage: str
    frequency: int
    period: int
    status: str
    start_date: Optional[str] = None
    memo: Optional[str] = None
    created_at: str


class MedListResponse(BaseModel):
    meds: List[Med]


class MedUpdate(BaseModel):
    dosage: Optional[str] = None
    frequency: Optional[int] = None
    period: Optional[int] = None
    memo: Optional[str] = None


class PillLookupRequest(BaseModel):
    color: Optional[str] = None
    shape: Optional[str] = None
    imprint: Optional[str] = None


class PillLookupResponse(BaseModel):
    name: str
    ingredient: str
    manufacturer: str
    image_url: Optional[str] = None


class DrugInfoResponse(BaseModel):
    name: str
    ingredient: str
    efficacy: Optional[str] = None
    caution: Optional[str] = None
    side_effects: Optional[list] = None
