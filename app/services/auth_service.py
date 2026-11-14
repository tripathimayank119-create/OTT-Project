from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.session import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.core.security import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def register(self, user_data: UserCreate) -> dict:
        """Register a new user."""
        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        hashed_password = pwd_context.hash(user_data.password)
        user = await self.user_repo.create(
            email=user_data.email, hashed_password=hashed_password
        )
        
        access_token = create_access_token(subject=user.email)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
            },
        }

    async def login(self, user_data: UserLogin) -> dict:
        """Login and get JWT token."""
        user = await self.user_repo.get_by_email(user_data.email)
        if not user or not pwd_context.verify(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        
        access_token = create_access_token(subject=user.email)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
            },
        }