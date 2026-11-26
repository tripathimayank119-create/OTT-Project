from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional

from app.database.session import get_session
from app.repositories.title_repository import TitleRepository
from app.schemas.title import TitleRead
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=List[TitleRead])
async def search_titles(
    session: AsyncSession = Depends(get_session),
    query: str = "",
    genre_id: Optional[int] = None,
    platform_id: Optional[int] = None,
    release_year_min: Optional[int] = None,
    release_year_max: Optional[int] = None,
    rating_min: Optional[float] = None,
    rating_max: Optional[float] = None,
) -> List[TitleRead]:
    """Advanced search with multiple filters."""
    service = SearchService(session)
    results = await service.advanced_search(
        query=query,
        genre_id=genre_id,
        platform_id=platform_id,
        release_year_min=release_year_min,
        release_year_max=release_year_max,
        rating_min=rating_min,
        rating_max=rating_max,
    )
    return results