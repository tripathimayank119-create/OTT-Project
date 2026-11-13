from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.database.session import get_session
from app.models.user import User
from app.schemas.user import UserRead
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: dict = Depends(get_current_user),
) -> UserRead:
    """Get current authenticated user profile."""
    return UserRead(
        id=current_user.get("id", 1),
        email=current_user.get("email", "user@example.com"),
        is_active=True,
        is_superuser=False,
        created_at=None,
    )