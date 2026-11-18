from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional, Dict, Any

from app.database.base import Base
from app.models.title import Title, Genre, Platform


class TitleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Title

    async def get_by_id(self, title_id: int) -> Optional[Title]:
        """Get title by ID."""
        result = await self.session.execute(
            select(self.model).where(self.model.id == title_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> List[Title]:
        """Get all titles with pagination."""
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def search(
        self,
        query: str = "",
        genre_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        release_year: Optional[int] = None,
    ) -> List[Title]:
        """Search titles with filters."""
        stmt = select(self.model)
        
        if query:
            stmt = stmt.where(
                self.model.title.ilike(f"%{query}%")
                | self.model.original_title.ilike(f"%{query}%")
            )
        
        if genre_id is not None:
            stmt = stmt.join(self.model.genre).where(Genre.id == genre_id)
        
        if platform_id is not None:
            stmt = stmt.join(self.model.platform).where(Platform.id == platform_id)
        
        if release_year is not None:
            stmt = stmt.where(self.model.release_year == release_year)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def search_advanced(
        self,
        query: str = "",
        genre_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        release_year_min: Optional[int] = None,
        release_year_max: Optional[int] = None,
        rating_min: Optional[float] = None,
        rating_max: Optional[float] = None,
    ) -> List[Title]:
        """Advanced search with multiple filters."""
        stmt = select(self.model)
        
        if query:
            stmt = stmt.where(
                self.model.title.ilike(f"%{query}%")
                | self.model.original_title.ilike(f"%{query}%")
            )
        
        if genre_id is not None:
            stmt = stmt.join(self.model.genre).where(Genre.id == genre_id)
        
        if platform_id is not None:
            stmt = stmt.join(self.model.platform).where(Platform.id == platform_id)
        
        if release_year_min is not None:
            stmt = stmt.where(self.model.release_year >= release_year_min)
        
        if release_year_max is not None:
            stmt = stmt.where(self.model.release_year <= release_year_max)
        
        if rating_min is not None:
            stmt = stmt.where(self.model.rating >= rating_min)
        
        if rating_max is not None:
            stmt = stmt.where(self.model.rating <= rating_max)
        
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_genres(self) -> List[Genre]:
        """Get all genres."""
        result = await self.session.execute(select(Genre))
        return result.scalars().all()

    async def get_platforms(self) -> List[Platform]:
        """Get all platforms."""
        result = await self.session.execute(select(Platform))
        return result.scalars().all()