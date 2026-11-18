
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost/ott_aggregator"
    )

    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class DevelopmentConfig(Settings):
    ENV: str = "development"
    DEBUG: bool = True


class ProductionConfig(Settings):
    ENV: str = "production"
    DEBUG: bool = False
