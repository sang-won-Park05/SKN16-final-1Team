from pydantic_settings import BaseSettings


class LLMSettings(BaseSettings):
    openai_api_key: str = ""
    opensearch_url: str | None = None

    class Config:
        env_file = ".env"
