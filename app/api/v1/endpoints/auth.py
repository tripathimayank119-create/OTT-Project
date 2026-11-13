from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.database.session import get_session
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.models.user import User
from app.core.security import create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    """Register a new user."""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["auto"], deprecated="auto")
    
    existing_user = await session.get(User, None)  # Placeholder
    # TODO: Check if user exists with same email
    
    hashed_password = pwd_context.hash(user_data.password)
    # TODO: Create user in database
    # new_user = User(email=user_data.email, hashed_password=hashed_password)
    # session.add(new_user)
    # await session.commit()
    # await session.refresh(new_user)
    
    # TODO: Generate token
    # access_token = create_access_token(subject=new_user.email)
    
    return UserRead(id=1, email=user_data.email, is_active=True, is_superuser=False, created_at=None)


@router.post("/login", response_model=Dict[str, str])
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> Dict[str, str]:
    """Login and get JWT token."""
    # TODO: Verify credentials
    # user = await session.execute(select(User).where(User.email == user_data.email))
    # user = user.scalar_one_or_none()
    # if not user or not pwd_context.verify(user_data.password, user.hashed_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    
    access_token = create_access_token(subject=user_data.email)
    return {"access_token": access_token, "token_type": "bearer"}