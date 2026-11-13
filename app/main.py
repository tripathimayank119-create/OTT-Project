from fastapi import FastAPI

from app.core.config import DevelopmentConfig
from app.api.v1.routers import include_routers

# Initialize FastAPI app
app = FastAPI(
    title="OTT Content Aggregator API",
    description="High-performance asynchronous OTT Content Aggregator API built with FastAPI, PostgreSQL, Redis and SQLAlchemy.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include all API routers
include_routers(app)


@app.get("/")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ott-content-aggregator-api",
        "version": "1.0.0",
    }