from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Secrets(BaseSettings):
    SECRET_KEY: str
    COMMON_PASSWORD: str
    DATABASE_URL: str
    
    # List of CORS origins via environment variable, comma-separated ideally or JSON string
    CORS_ORIGINS: List[str]
    
    # Toggle secure behavior (like HTTPS-only cookies, HSTS) for dev/prod
    ENVIRONMENT: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

secrets = Secrets()