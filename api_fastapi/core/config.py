from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    llm_service_url: str = "http://localhost:8001"
    stt_service_url: str = "http://localhost:8002"
    ocr_service_url: str = "http://localhost:8003"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
