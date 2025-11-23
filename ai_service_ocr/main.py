from fastapi import FastAPI
from api import ocr

app = FastAPI(title="OCR Service", version="0.1.0")
app.include_router(ocr.router, prefix="/internal/ocr", tags=["ocr"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
