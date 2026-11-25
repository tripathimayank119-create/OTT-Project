import os


class Settings:
    """Application settings."""
    ENV: str = os.environ.get("ENV", "development")
    DEBUG: bool = os.environ.get("DEBUG", "True").lower() == "true"
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/ott_aggregator"
    )
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class DevelopmentConfig(Settings):
    """Development configuration."""
    pass


class ProductionConfig(Settings):
    """Production configuration."""
    ENV: str = "production"
    DEBUG: bool = False


settings = Settings()