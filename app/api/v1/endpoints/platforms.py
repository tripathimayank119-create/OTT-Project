from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.database.session import get_session
from app.models.title import Platform
from app.schemas.title import PlatformRead
from app.repositories.title_repository import TitleRepository

router = APIRouter(prefix="/platforms", tags=["Platforms"])


@router.get("/", response_model=List[PlatformRead])
async def list_platforms(
    session: AsyncSession = Depends(get_session),
) -> List[PlatformRead]:
    """List all OTT platforms."""
    repo = TitleRepository(session)
    platforms = await repo.get_platforms()
    return platforms