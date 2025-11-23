from fastapi import APIRouter
from ..schemas.health_record import HealthRecordCreate, HealthRecordResponse

router = APIRouter()
_fake_store: list[HealthRecordResponse] = []


@router.post("/", response_model=HealthRecordResponse)
def create_health_record(payload: HealthRecordCreate) -> HealthRecordResponse:
    record = HealthRecordResponse(id=len(_fake_store) + 1, **payload.model_dump())
    _fake_store.append(record)
    return record


@router.get("/", response_model=list[HealthRecordResponse])
def list_health_records() -> list[HealthRecordResponse]:
    return _fake_store
