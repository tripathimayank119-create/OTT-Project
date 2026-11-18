from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional

from app.models.title import Title
from app.repositories.title_repository import TitleRepository


class SearchService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.title_repo = TitleRepository(session)

    async def advanced_search(
        self,
        query: str,
        genre_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        release_year_min: Optional[int] = None,
        release_year_max: Optional[int] = None,
        rating_min: Optional[float] = None,
        rating_max: Optional[float] = None,
    ) -> List[Title]:
        """Advanced search with multiple filters."""
        results = await self.title_repo.search_advanced(
            query=query,
            genre_id=genre_id,
            platform_id=platform_id,
            release_year_min=release_year_min,
            release_year_max=release_year_max,
            rating_min=rating_min,
            rating_max=rating_max,
        )
        return results