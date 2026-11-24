import os

class Settings:
    """Application settings."""
    ENV: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost/ott_aggregator"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class DevelopmentConfig(Settings):
    """Development configuration."""
    pass


class ProductionConfig(Settings):
    """Production configuration."""
    ENV: str = "production"
    DEBUG: bool = False