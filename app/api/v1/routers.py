from fastapi import APIRouter

# Authentication router
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Users router
users_router = APIRouter(prefix="/users", tags=["Users"])

# Titles router
titles_router = APIRouter(prefix="/titles", tags=["Titles"])

# Genres router
genres_router = APIRouter(prefix="/genres", tags=["Genres"])

# Platforms router
platforms_router = APIRouter(prefix="/platforms", tags=["Platforms"])

# Search router
search_router = APIRouter(prefix="/search", tags=["Search"])

# Sync router
sync_router = APIRouter(prefix="/sync", tags=["Background"])

# Register all routers at api/v1 level
def include_routers(app):
    """Include all API routers into the FastAPI app."""
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(titles_router)
    app.include_router(genres_router)
    app.include_router(platforms_router)
    app.include_router(search_router)
    app.include_router(sync_router)