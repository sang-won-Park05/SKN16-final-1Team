def redact(text: str) -> str:
    return text.replace("patient", "[redacted]")
