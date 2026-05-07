from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Secrets(BaseSettings):
    SECRET_KEY: str
    COMMON_PASSWORD: str
    DATABASE_URL: str
    
    # Accept the raw environment value for CORS origins. Jenkins may inject
    # a single-quoted JSON string (e.g. '\'["https://a","https://b"]\'')
    # which would break strict JSON parsing at load time. We accept a string
    # here and parse it in the application runtime where we can be more forgiving.
    CORS_ORIGINS: str
    
    # Toggle secure behavior (like HTTPS-only cookies, HSTS) for dev/prod
    ENVIRONMENT: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

secrets = Secrets()