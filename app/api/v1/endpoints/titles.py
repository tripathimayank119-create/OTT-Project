from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.database.session import get_session
from app.models.title import Title, Genre, Platform
from app.schemas.title import TitleRead, TitleCreate, TitleUpdate, GenreRead, PlatformRead
from app.repositories.title_repository import TitleRepository
from app.schemas.user import UserCreate
from app.utils.pagination import PaginationParams, paginate

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
    # Create title without genre/platform IDs first, then handle relationships
    title_dict = title_data.dict(exclude={"genre_ids", "platform_ids"})
    title = await repo.create(title_dict)
    
    # Handle genre relationships if provided
    if title_data.genre_ids:
        from sqlalchemy import select
        for genre_id in title_data.genre_ids:
            genre = await session.get(Genre, genre_id)
            if genre:
                title.genre.append(genre)
    
    # Handle platform relationships if provided
    if title_data.platform_ids:
        from sqlalchemy import select
        for platform_id in title_data.platform_ids:
            platform = await session.get(Platform, platform_id)
            if platform:
                title.platform.append(platform)
    
    await session.flush()
    await session.refresh(title)
    await session.commit()
    return title


@router.get("/", response_model=List[TitleRead])
async def list_titles(
    pagination: PaginationParams = Depends(),
    session: AsyncSession = Depends(get_session),
) -> List[TitleRead]:
    """List all titles with pagination."""
    repo = TitleRepository(session)
    titles = await repo.get_all(skip=pagination.skip, limit=pagination.limit)
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