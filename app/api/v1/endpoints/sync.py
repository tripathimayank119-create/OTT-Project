
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.services.content_sync import sync_catalogue


router = APIRouter(
    prefix="/sync",
    tags=["Content Synchronization"],
)


@router.post("/catalogue")
async def synchronize_catalogue(
    catalogue_data: List[Dict[str, Any]],
    session: AsyncSession = Depends(get_session),
):
    """
    Synchronize catalogue data with the database.

    New titles are added.
    Existing titles are updated.
    Genres and platforms are resolved automatically.
    """

    result = await sync_catalogue(
        catalogue_data=catalogue_data,
        session=session,
    )

    return result
