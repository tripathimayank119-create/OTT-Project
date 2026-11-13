from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.database.session import get_session
from app.models.title import Genre
from app.schemas.title import GenreRead
from app.repositories.title_repository import TitleRepository

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("/", response_model=List[GenreRead])
async def list_genres(
    session: AsyncSession = Depends(get_session),
) -> List[GenreRead]:
    """List all genres."""
    repo = TitleRepository(session)
    genres = await repo.get_genres()
    return genres