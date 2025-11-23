from fastapi import FastAPI
from services.llm_service import LLMService
from api import llm

app = FastAPI(title="LLM Service", version="0.1.0")
app.state.llm_service = LLMService()
app.include_router(llm.router, prefix="/internal/llm", tags=["llm"])


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok"}
