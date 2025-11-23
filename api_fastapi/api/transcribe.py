from fastapi import APIRouter, HTTPException
import requests
from ..core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/stt")
def transcribe_audio(payload: dict) -> dict:
    """Send audio payload to STT microservice."""
    try:
        response = requests.post(
            f"{settings.stt_service_url}/internal/stt/transcribe",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"STT service unavailable: {exc}") from exc
    return response.json()
