from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class HealthProfile(BaseModel):
    height: Optional[float] = None
    weight: Optional[float] = None
    blood_type: Optional[str] = None
    drinking: Optional[str] = None
    smoking: Optional[str] = None


class HealthHistoryItem(BaseModel):
    version: int
    changes: Dict[str, Any]
    changed_at: str


class ConditionCreate(BaseModel):
    condition_name: str
    type: Optional[str] = None
    diagnosis_date: Optional[str] = None
    status: Optional[str] = None
    note: Optional[str] = None


class Condition(BaseModel):
    id: str
    condition_name: str
    status: Optional[str] = None
    type: Optional[str] = None
    diagnosis_date: Optional[str] = None
    note: Optional[str] = None
    updated_at: Optional[str] = None
    created_at: Optional[str] = None


class AllergyCreate(BaseModel):
    allergen: str
    reaction: Optional[str] = None
    severity: Optional[str] = None
    noted_at: Optional[str] = None
    note: Optional[str] = None


class Allergy(BaseModel):
    id: str
    allergen: str
    severity: Optional[str] = None


class MessageResponse(BaseModel):
    message: str
