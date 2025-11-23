FORBIDDEN_KEYWORDS = {"suicide", "self-harm"}


def is_safe(prompt: str) -> bool:
    return not any(keyword in prompt.lower() for keyword in FORBIDDEN_KEYWORDS)
