
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.database.session import get_session
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False,
)


async def get_db_session():
    """Provide an asynchronous database session."""
    async for session in get_session():
        yield session


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
):
    """Validate JWT and retrieve the user by database ID."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")

        if not subject:
            raise credentials_exception

        user_id = int(subject)

        if user_id <= 0:
            raise credentials_exception

    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)

    if user is None or not user.is_active:
        raise credentials_exception

    return user


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db_session),
):
    """Return the authenticated user or None."""

    if not token:
        return None

    try:
        return await get_current_user(token, session)
    except HTTPException:
        return None
