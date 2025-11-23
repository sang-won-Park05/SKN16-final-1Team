from enum import Enum


class DocumentType(str, Enum):
    prescription = "prescription"
    visit_summary = "visit_summary"
