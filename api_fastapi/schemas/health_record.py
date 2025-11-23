from pydantic import BaseModel


class HealthRecordCreate(BaseModel):
    patient_name: str
    description: str


class HealthRecordResponse(HealthRecordCreate):
    id: int
