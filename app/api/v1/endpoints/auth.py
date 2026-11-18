
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.database.session import get_session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserRead


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """Register a new user account."""

    user_repo = UserRepository(session)

    email = str(user_data.email).lower()

    # Check whether the email is already registered.
    existing_user = await user_repo.get_by_email(email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Hash the password before storing it.
    hashed_password = pwd_context.hash(user_data.password)

    try:
        user = await user_repo.create(
            email=email,
            hashed_password=hashed_password,
        )

        await session.commit()
        await session.refresh(user)

    except Exception:
        await session.rollback()
        raise

    return user


@router.post("/login")
async def login(
    user_data: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    """Authenticate a user and generate a JWT access token."""

    user_repo = UserRepository(session)

    email = str(user_data.email).lower()

    user = await user_repo.get_by_email(email)

    # Validate email and password.
    if (
        not user
        or not pwd_context.verify(
            user_data.password,
            user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Prevent inactive users from logging in.
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive",
        )

    # Generate JWT using the user's database ID.
    access_token = create_access_token(
        subject=user.id,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
