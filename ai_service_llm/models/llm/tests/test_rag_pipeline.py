from models.llm.core import orchestrator


def test_run_rag_pipeline_returns_answer():
    result = orchestrator.run_rag_pipeline("What is a headache?", context="sample")
    assert "answer" in result
    assert isinstance(result["source_documents"], list)
