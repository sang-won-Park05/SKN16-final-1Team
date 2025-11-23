from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.llm_service import LLMService

router = APIRouter()


class LLMRequest(BaseModel):
    question: str
    context: str | None = None


def get_service():
    return LLMService()


@router.post("/query")
def query(request: LLMRequest, service: LLMService = Depends(get_service)) -> dict:
    return service.query(request.question, request.context)
