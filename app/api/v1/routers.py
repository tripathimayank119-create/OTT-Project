
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    titles,
    genres,
    platforms,
    sync,
)


api_router = APIRouter()


# Authentication
api_router.include_router(auth.router)

# User Management
api_router.include_router(users.router)

# OTT Catalogue
api_router.include_router(titles.router)
api_router.include_router(genres.router)
api_router.include_router(platforms.router)

# Background Catalogue Synchronization
api_router.include_router(sync.router)


def include_routers(app):
    app.include_router(api_router)
