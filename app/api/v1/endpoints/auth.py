from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.database.session import get_session
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.models.user import User
from app.core.security import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    """Register a new user."""
    from app.repositories.user_repository import UserRepository
    user_repo = UserRepository(session)
    
    # Check if user already exists
    existing_user = await user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    hashed_password = pwd_context.hash(user_data.password)
    user = await user_repo.create(
        email=user_data.email, hashed_password=hashed_password
    )
    
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
    from app.repositories.user_repository import UserRepository
    user_repo = UserRepository(session)
    
    user = await user_repo.get_by_email(user_data.email)
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}