from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.database.session import get_session
from app.models.title import Title

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=List[TitleRead])
async def search_titles(
    session: AsyncSession = Depends(get_session),
    query: str = "",
    genre_id: int = 0,
    platform_id: int = 0,
    release_year: int = 0,
) -> List[TitleRead]:
    """Search titles with filters."""
    repo = TitleRepository(session)
    results = await repo.search(
        query=query,
        genre_id=genre_id if genre_id > 0 else None,
        platform_id=platform_id if platform_id > 0 else None,
        release_year=release_year if release_year > 0 else None,
    )
    return results