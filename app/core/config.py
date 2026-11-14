
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "development"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/ott_aggregator"
    )
    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "change-this-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class DevelopmentConfig(Settings):
    ENV: str = "development"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True


class ProductionConfig(Settings):
    ENV: str = "production"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False


settings = Settings()
