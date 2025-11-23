from fastapi import APIRouter, HTTPException
import requests
from ..core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/query")
def query_llm(payload: dict) -> dict:
    """Proxy user query to the LLM microservice."""
    try:
        response = requests.post(
            f"{settings.llm_service_url}/internal/llm/query",
            json={"question": payload.get("question"), "context": payload.get("context")},
            timeout=20,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"LLM service unavailable: {exc}") from exc
    return response.json()
