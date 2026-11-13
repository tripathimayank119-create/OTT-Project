from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.config import Settings
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_db_session():
    """Dependency to get async database session."""
    # This will be overridden with actual session factory
    from app.database.session import get_session
    async for session in get_session():
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """Dependency to get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # TODO: Fetch user from database
    return {"id": user_id, "email": "user@example.com"}

async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
) -> Optional[dict]:
    """Dependency to get current user optionally (for public endpoints)."""
    if token is None:
        return None
    try:
        return await get_current_user(token, session)
    except HTTPException:
        return None