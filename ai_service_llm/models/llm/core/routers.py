def route_query(question: str) -> str:
    return "medical" if "pain" in question.lower() else "general"
