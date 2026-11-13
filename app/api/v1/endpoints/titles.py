from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.database.session import get_session
from app.models.title import Title, Genre, Platform
from app.schemas.title import TitleRead, TitleCreate, TitleUpdate, GenreRead, PlatformRead
from app.repositories.title_repository import TitleRepository
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/titles", tags=["Titles"])


@router.post(
    "/", response_model=TitleRead, status_code=status.HTTP_201_CREATED
)
async def create_title(
    title_data: TitleCreate,
    session: AsyncSession = Depends(get_session),
) -> TitleRead:
    """Create a new title (movie/TV show)."""
    repo = TitleRepository(session)
    title = await repo.create(title_data.dict(exclude={"genre_ids", "platform_ids"}))
    # TODO: Handle genre and platform relationships
    return title


@router.get("/", response_model=List[TitleRead])
async def list_titles(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
) -> List[TitleRead]:
    """List all titles with pagination."""
    repo = TitleRepository(session)
    titles = await repo.get_all(skip=skip, limit=limit)
    return titles


@router.get("/{title_id}", response_model=TitleRead)
async def get_title(
    title_id: int,
    session: AsyncSession = Depends(get_session),
) -> TitleRead:
    """Get a title by ID."""
    repo = TitleRepository(session)
    title = await repo.get_by_id(title_id)
    if not title:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Title not found",
        )
    return title