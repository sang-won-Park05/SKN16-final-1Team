from fastapi import APIRouter, Depends, HTTPException
from api_fastapi.api.deps import get_current_user
from api_fastapi.schemas.chatbot import (
    ChatQuery,
    ChatResponse,
    ChatHistoryResponse,
    ChatHistoryItem,
    VoiceQuery,
    VoiceResponse,
    MessageResponse,
)
from api_fastapi.core.database import db

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/query", response_model=ChatResponse)
async def query(payload: ChatQuery, user=Depends(get_current_user)) -> ChatResponse:
    history = db.chat_history.setdefault(user["id"], [])
    entry_id = payload.id or db.next_id("chat")
    answer = f"LLM 응답: {payload.query}"
    record = {"id": entry_id, "query": payload.query, "answer": answer, "created_at": db.now()}
    history.append(record)
    return ChatResponse(id=entry_id, answer=answer, sources=["visits#123", "drugs#11"], used_model=payload.model or "gpt-4", latency=1240)


@router.get("/history", response_model=ChatHistoryResponse)
async def history(limit: int = 20, order: str = "desc", user=Depends(get_current_user)) -> ChatHistoryResponse:
    items = db.chat_history.get(user["id"], [])
    if order == "desc":
        items = list(reversed(items))
    items = items[:limit]
    return ChatHistoryResponse(history=[ChatHistoryItem(**h) for h in items])


@router.get("/history/{history_id}", response_model=dict)
async def history_detail(history_id: str, user=Depends(get_current_user)) -> dict:
    items = db.chat_history.get(user["id"], [])
    target = next((h for h in items if h["id"] == history_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없음")
    return {"id": target["id"], "messages": [
        {"role": "user", "content": target["query"], "timestamp": target["created_at"]},
        {"role": "assistant", "content": target["answer"], "timestamp": target["created_at"]},
    ]}


@router.delete("/history/{history_id}", response_model=MessageResponse)
async def delete_history(history_id: str, user=Depends(get_current_user)) -> MessageResponse:
    items = db.chat_history.get(user["id"], [])
    db.chat_history[user["id"]] = [h for h in items if h["id"] != history_id]
    return MessageResponse(message="대화 세션이 삭제되었습니다")


@router.delete("/history", response_model=MessageResponse)
async def clear_history(user=Depends(get_current_user)) -> MessageResponse:
    db.chat_history[user["id"]] = []
    return MessageResponse(message="모든 대화 이력이 삭제되었습니다")


@router.post("/voice", response_model=VoiceResponse)
async def voice(payload: VoiceQuery, user=Depends(get_current_user)) -> VoiceResponse:
    entry_id = payload.id or db.next_id("chat")
    stt_text = "최근 복용약 알려줘"
    answer = "최근 복용한 약은 타이레놀입니다." if payload.auto_query else None
    status = "completed"
    return VoiceResponse(id=entry_id, stt_text=stt_text, answer=answer, status=status)
