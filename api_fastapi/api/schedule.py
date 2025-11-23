from fastapi import APIRouter, Depends, HTTPException, Query
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.schedule import (
    ScheduleCreate,
    Schedule,
    ScheduleListResponse,
    ScheduleUpdate,
    CalendarResponse,
    MedSchedule,
    MedCheckRequest,
    MessageResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/calendar", response_model=CalendarResponse)
async def calendar(year: int, month: int, user=Depends(get_current_user)) -> CalendarResponse:
    events = [Schedule(**s) for s in db.schedules.values() if s.get("date", "").startswith(f"{year}-{month:02d}")]
    days = sorted({s.date for s in events})
    return CalendarResponse(days=list(days), events=events)


@router.post("/", response_model=Schedule, status_code=201)
async def create_schedule(payload: ScheduleCreate, user=Depends(get_current_user)) -> Schedule:
    sid = db.next_id("sch")
    record = payload.model_dump(exclude_none=True)
    record.update({"id": sid, "created_at": db.now()})
    db.schedules[sid] = record
    return Schedule(**record)


@router.get("/", response_model=ScheduleListResponse)
async def list_schedule(
    from_: str | None = Query(default=None, alias="from"),
    to: str | None = None,
    type: str | None = None,
    page: int = 1,
    size: int = 20,
    user=Depends(get_current_user),
) -> ScheduleListResponse:
    items = list(db.schedules.values())
    if type:
        items = [s for s in items if s.get("type") == type]
    start = (page - 1) * size
    end = start + size
    sliced = items[start:end]
    return ScheduleListResponse(schedules=[Schedule(**s) for s in sliced], pagination={"page": page, "total": len(items)})


@router.get("/{schedule_id}", response_model=Schedule)
async def get_schedule(schedule_id: str, user=Depends(get_current_user)) -> Schedule:
    sched = db.schedules.get(schedule_id)
    if not sched:
        raise HTTPException(status_code=404, detail="대상 없음")
    return Schedule(**sched)


@router.patch("/{schedule_id}", response_model=MessageResponse)
async def update_schedule(schedule_id: str, payload: ScheduleUpdate, user=Depends(get_current_user)) -> MessageResponse:
    sched = db.schedules.get(schedule_id)
    if not sched:
        raise HTTPException(status_code=404, detail="대상 없음")
    sched.update(payload.model_dump(exclude_none=True))
    db.schedules[schedule_id] = sched
    return MessageResponse(message="일정이 수정되었습니다")


@router.delete("/{schedule_id}", response_model=MessageResponse)
async def delete_schedule(schedule_id: str, user=Depends(get_current_user)) -> MessageResponse:
    db.schedules.pop(schedule_id, None)
    return MessageResponse(message="일정이 삭제되었습니다")


@router.get("/meds", response_model=dict)
async def med_schedules(user=Depends(get_current_user)) -> dict:
    items = [MedSchedule(**m) for m in db.med_schedules.values()]
    return {"meds": items}


@router.patch("/meds/{med_sched_id}/check", response_model=MessageResponse)
async def check_med(med_sched_id: str, payload: MedCheckRequest, user=Depends(get_current_user)) -> MessageResponse:
    sched = db.med_schedules.get(med_sched_id)
    if not sched:
        raise HTTPException(status_code=404, detail="대상 없음")
    sched["status"] = "done" if payload.done else "pending"
    db.med_schedules[med_sched_id] = sched
    return MessageResponse(message="복약 완료로 표시되었습니다")
