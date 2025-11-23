from pydantic import BaseModel
from .types import DocumentType


class OCRRequest(BaseModel):
    image_b64: str
    document_type: DocumentType = DocumentType.prescription


class OCRItem(BaseModel):
    field: str
    value: str


class OCRResponse(BaseModel):
    items: list[OCRItem]
