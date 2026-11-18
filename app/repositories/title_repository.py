
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.title import Title, Genre, Platform


class TitleRepository:
    """Database operations for OTT titles."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Title

    async def create(self, data: dict) -> Title:
        """Create and persist a new title."""
        title = Title(**data)
        self.session.add(title)
        await self.session.flush()
        await self.session.refresh(title)
        return title

    async def get_by_id(self, title_id: int) -> Optional[Title]:
        """Retrieve a title by ID with its relationships."""
        result = await self.session.execute(
            select(Title)
            .options(
                selectinload(Title.genres),
                selectinload(Title.platforms),
            )
            .where(Title.id == title_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Title]:
        """Retrieve titles with pagination."""
        result = await self.session.execute(
            select(Title)
            .options(
                selectinload(Title.genres),
                selectinload(Title.platforms),
            )
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def search(
        self,
        query: str = "",
        genre_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        release_year: Optional[int] = None,
    ) -> List[Title]:
        """Search titles using optional filters."""
        stmt = select(Title).options(
            selectinload(Title.genres),
            selectinload(Title.platforms),
        )

        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(
                Title.title.ilike(pattern)
                | Title.original_title.ilike(pattern)
            )

        if genre_id is not None:
            stmt = stmt.join(Title.genres).where(
                Genre.id == genre_id
            )

        if platform_id is not None:
            stmt = stmt.join(Title.platforms).where(
                Platform.id == platform_id
            )

        if release_year is not None:
            stmt = stmt.where(
                Title.release_year == release_year
            )

        stmt = stmt.distinct()

        result = await self.session.execute(stmt)
        return list(result.scalars().unique().all())

    async def get_genres(self) -> List[Genre]:
        """Retrieve all genres."""
        result = await self.session.execute(
            select(Genre).order_by(Genre.name)
        )
        return list(result.scalars().all())

    async def get_platforms(self) -> List[Platform]:
        """Retrieve all OTT platforms."""
        result = await self.session.execute(
            select(Platform).order_by(Platform.name)
        )
        return list(result.scalars().all())

    async def delete(self, title: Title) -> None:
        """Delete a title."""
        await self.session.delete(title)
        await self.session.flush()
