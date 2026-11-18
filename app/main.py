
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import include_routers


# Initialize FastAPI application
app = FastAPI(
    title="OTT Content Aggregator API",
    description=(
        "High-performance asynchronous OTT Content Aggregator API "
        "built with FastAPI, PostgreSQL, Redis and SQLAlchemy."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
include_routers(app)


# Health Check Endpoint
@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "ott-content-aggregator-api",
        "version": "1.0.0",
    }
