def retrieve_documents(query: str) -> list[dict]:
    return [{"id": 1, "score": 1.0, "text": f"Stub doc for: {query}"}]
