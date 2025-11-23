from pydantic import BaseModel
from typing import Optional, List


class ScheduleCreate(BaseModel):
    title: str
    type: str
    date: str
    time: Optional[str] = None
    location: Optional[str] = None
    memo: Optional[str] = None


class Schedule(BaseModel):
    id: str
    title: str
    type: str
    date: str
    time: Optional[str] = None
    location: Optional[str] = None
    memo: Optional[str] = None
    created_at: Optional[str] = None


class ScheduleListResponse(BaseModel):
    schedules: List[Schedule]
    pagination: dict


class ScheduleUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    memo: Optional[str] = None


class CalendarResponse(BaseModel):
    days: List[str]
    events: List[Schedule]


class MedSchedule(BaseModel):
    id: str
    drug_name: str
    time: str
    status: str


class MedCheckRequest(BaseModel):
    done: bool


class MessageResponse(BaseModel):
    message: str
