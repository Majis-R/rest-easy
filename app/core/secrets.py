from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Secrets(BaseSettings):
    SECRET_KEY: str
    COMMON_PASSWORD: str
    DATABASE_URL: str
    
    CORS_ORIGINS: List[str] = [
        "http://localhost",
        "https://localhost",
        "http://127.0.0.1",
        "https://127.0.0.1",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://majis-r.github.io",
    ]
    
    # Toggle secure behavior (like HTTPS-only cookies, HSTS) for dev/prod
    ENVIRONMENT: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

secrets = Secrets()