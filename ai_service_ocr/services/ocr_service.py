from models.ocr.core.schemas import OCRRequest, OCRResponse
from models.ocr.pipelines import prescription_ocr, visit_summary_ocr
from models.ocr.core.types import DocumentType


def run_ocr(request: OCRRequest) -> OCRResponse:
    if request.document_type == DocumentType.prescription:
        return prescription_ocr.run_pipeline(request)
    return visit_summary_ocr.run_pipeline(request)
