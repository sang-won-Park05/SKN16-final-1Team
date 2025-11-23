from ..core.schemas import OCRRequest, OCRResponse, OCRItem
from ..utils import image_preprocess, postprocess
from ..engine import openai_vision


def run_pipeline(request: OCRRequest) -> OCRResponse:
    normalized_image = image_preprocess.normalize_image(request.image_b64)
    _ = normalized_image
    raw = openai_vision.call_vision_model("prescription", normalized_image)
    items = [OCRItem(field="medication", value=postprocess.normalize_units(raw))]
    return OCRResponse(items=items)
