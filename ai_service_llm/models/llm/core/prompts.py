system_prompt = "You are a helpful medical assistant."


def format_prompt(question: str, context: str | None = None) -> str:
    if context:
        return f"{system_prompt}\nContext: {context}\nQuestion: {question}"
    return f"{system_prompt}\nQuestion: {question}"
