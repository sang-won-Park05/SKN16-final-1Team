from fastapi import APIRouter
from models.ocr.core.schemas import OCRRequest, OCRResponse
from services.ocr_service import run_ocr

router = APIRouter()


@router.post("/prescription", response_model=OCRResponse)
@router.post("/visit", response_model=OCRResponse)
def ocr_endpoint(request: OCRRequest) -> OCRResponse:
    return run_ocr(request)
