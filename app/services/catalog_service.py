from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.models.title import Title, Genre, Platform
from app.repositories.title_repository import TitleRepository


class CatalogService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.title_repo = TitleRepository(session)

    async def create_title(self, title_data: dict) -> Title:
        """Create a new title."""
        repo = TitleRepository(self.session)
        title = await repo.create(title_data)
        return title

    async def get_title(self, title_id: int) -> Optional[Title]:
        """Get title by ID."""
        return await self.title_repo.get_by_id(title_id)

    async def list_titles(
        self, skip: int = 0, limit: int = 100
    ) -> List[Title]:
        """List all titles."""
        return await self.title_repo.get_all(skip=skip, limit=limit)

    async def search_titles(
        self,
        query: str = "",
        genre_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        release_year: Optional[int] = None,
    ) -> List[Title]:
        """Search titles with filters."""
        return await self.title_repo.search(
            query=query,
            genre_id=genre_id,
            platform_id=platform_id,
            release_year=release_year,
        )

    async def list_genres(self) -> List[Genre]:
        """List all genres."""
        return await self.title_repo.get_genres()

    async def list_platforms(self) -> List[Platform]:
        """List all platforms."""
        return await self.title_repo.get_platforms()