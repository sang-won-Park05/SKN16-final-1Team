from pydantic import BaseModel
from typing import Optional, List


class ChatQuery(BaseModel):
    id: Optional[str] = None
    query: str
    context: Optional[bool] = None
    model: Optional[str] = None
    temperature: Optional[float] = None


class ChatResponse(BaseModel):
    id: str
    answer: str
    sources: Optional[List[str]] = None
    used_model: Optional[str] = None
    latency: Optional[int] = None


class ChatHistoryItem(BaseModel):
    id: str
    query: str
    answer: str
    created_at: str


class ChatHistoryResponse(BaseModel):
    history: List[ChatHistoryItem]


class VoiceQuery(BaseModel):
    id: Optional[str] = None
    file_id: Optional[str] = None
    auto_query: Optional[bool] = None


class VoiceResponse(BaseModel):
    id: str
    stt_text: str
    answer: Optional[str] = None
    status: str


class MessageResponse(BaseModel):
    message: str
