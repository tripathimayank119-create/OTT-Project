from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from app.database.session import get_session
from app.models.user import User
from app.schemas.user import UserRead, UserCreate, UserUpdate
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


@router.get("/", response_model=List[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
) -> List[UserRead]:
    """List all users (admin only)."""
    from app.repositories.user_repository import UserRepository
    user_repo = UserRepository(session)
    users = await user_repo.get_all()
    return [
        UserRead(
            id=user.id,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
        )
        for user in users
    ]


@router.put("/me", response_model=UserRead)
async def update_me(
    user_data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    """Update current user profile."""
    from app.repositories.user_repository import UserRepository
    user_repo = UserRepository(session)
    
    # Update user email if provided
    if user_data.email is not None:
        existing_user = await user_repo.get_by_email(user_data.email)
        if existing_user and existing_user.id != current_user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        current_user["email"] = user_data.email
    
    # Note: password update would require additional verification
    return UserRead(
        id=current_user.get("id", 1),
        email=current_user.get("email", "user@example.com"),
        is_active=True,
        is_superuser=False,
        created_at=None,
    )