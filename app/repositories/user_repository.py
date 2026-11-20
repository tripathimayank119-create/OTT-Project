from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database.base import Base
from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = User

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, email: str, hashed_password: str) -> User:
        """Create a new user."""
        user = self.model(email=email, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_all(self) -> List[User]:
        """Get all users."""
        result = await self.session.execute(select(self.model))
        return result.scalars().all()