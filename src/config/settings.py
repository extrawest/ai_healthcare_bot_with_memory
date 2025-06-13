from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = Field(default="0.0.0.0", description="Host address")
    port: int = Field(default=8000, description="Port number")
    ui_port: int = Field(default=8001, description="UI port number")

    qdrant_port: int = Field(default=6333, description="Qdrant port")
    qdrant_host: str = Field(default="localhost", description="Qdrant host")

    openai_api_key: str = Field(default="api_key", description="OpenAI API key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

settings = Settings()