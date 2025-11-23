from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_fastapi.api import (
    auth,
    user,
    admin,
    health,
    drugs,
    visits,
    schedule,
    chatbot,
    files,
    stt,
)

app = FastAPI(title="Medinote API", version="0.1.0")

# CORS 설정: 프론트 개발 서버(5173) 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(health.router)
app.include_router(drugs.router)
app.include_router(visits.router)
app.include_router(schedule.router)
app.include_router(chatbot.router)
app.include_router(files.router)
app.include_router(stt.router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}
