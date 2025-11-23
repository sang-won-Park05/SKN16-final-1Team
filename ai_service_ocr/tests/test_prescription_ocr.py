from models.ocr.core.schemas import OCRRequest
from models.ocr.pipelines import prescription_ocr


def test_prescription_pipeline_returns_items():
    request = OCRRequest(image_b64="dGVzdA==")
    response = prescription_ocr.run_pipeline(request)
    assert response.items
