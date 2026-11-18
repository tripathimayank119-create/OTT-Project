
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Database operations for user authentication and management."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        """Find a user using their email address."""

        result = await self.session.execute(
            select(User).where(User.email == email.lower())
        )

        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Find a user using their database ID."""

        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        hashed_password: str,
    ) -> User:
        """Create a new user account."""

        user = User(
            email=email.lower(),
            hashed_password=hashed_password,
        )

        self.session.add(user)

        await self.session.flush()

        return user
