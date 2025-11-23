from models.llm.core import orchestrator
from models.llm.core.utils import preprocess


class LLMService:
    def query(self, question: str, context: str | None = None) -> dict:
        cleaned = preprocess.clean_question(question)
        return orchestrator.run_rag_pipeline(cleaned, context=context)
