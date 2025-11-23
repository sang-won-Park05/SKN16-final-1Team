def rerank(documents: list[dict]) -> list[dict]:
    return sorted(documents, key=lambda item: item.get("score", 0), reverse=True)
