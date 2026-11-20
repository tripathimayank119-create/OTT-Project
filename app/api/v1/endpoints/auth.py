from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.database.session import get_session
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.models.user import User
from app.core.security import create_access_token
from app.core.dependencies import get_current_user
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    """Register a new user."""
    auth_service = AuthService(session)
    user = await auth_service.register(user_data.email, user_data.password)
    access_token = create_access_token(subject=user.email)
    return UserRead(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at,
    )


@router.post("/login", response_model=Dict[str, str])
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> Dict[str, str]:
    """Login and get JWT token."""
    auth_service = AuthService(session)
    tokens = await auth_service.login(user_data.email, user_data.password)
    return tokens