from pydantic_settings import BaseSettings, SettingsConfigDict

class Secrets(BaseSettings):
    secret_key: str
    set_password: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

secrets = Secrets()