from pydantic_settings import BaseSettings, SettingsConfigDict

class Secrets(BaseSettings):
    SECRET_KEY: str
    COMMON_PASSWORD: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

secrets = Secrets()