from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    database_url: str = "sqlite:///database.db"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()