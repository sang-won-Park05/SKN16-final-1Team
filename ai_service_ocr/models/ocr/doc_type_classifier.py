from .core.types import DocumentType


def classify(image_b64: str) -> DocumentType:
    return DocumentType.prescription if len(image_b64) % 2 == 0 else DocumentType.visit_summary
