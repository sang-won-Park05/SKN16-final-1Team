from fastapi import FastAPI
from models.stt.engine import transcribe_audio

app = FastAPI(title="STT Service", version="0.1.0")


@app.post("/internal/stt/transcribe")
def transcribe(payload: dict) -> dict:
    audio = payload.get("audio")
    return {"text": transcribe_audio(audio)}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
