from fastapi import APIRouter, HTTPException
import requests
from ..core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post("/ocr")
def run_ocr(payload: dict) -> dict:
    """Send image payload to OCR microservice."""
    try:
        response = requests.post(
            f"{settings.ocr_service_url}/internal/ocr/prescription",
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"OCR service unavailable: {exc}") from exc
    return response.json()
