from . import prompts, retriever, reranker, guards


def run_rag_pipeline(question: str, context: str | None = None) -> dict:
    if not guards.is_safe(question):
        return {"answer": "I cannot answer unsafe requests.", "source_documents": []}

    documents = retriever.retrieve_documents(question)
    ranked = reranker.rerank(documents)
    prompt = prompts.format_prompt(question, context)
    answer = f"Stubbed answer to: {prompt}"
    return {"answer": answer, "source_documents": ranked}
