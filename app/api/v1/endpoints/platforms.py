
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.title import Platform
from app.schemas.title import PlatformCreate, PlatformRead


router = APIRouter(
    prefix="/platforms",
    tags=["Platforms"],
)


# GET ALL PLATFORMS
@router.get(
    "/",
    response_model=List[PlatformRead],
)
async def list_platforms(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Platform).order_by(Platform.name)
    )

    return result.scalars().all()


# CREATE PLATFORM
@router.post(
    "/",
    response_model=PlatformRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_platform(
    platform_data: PlatformCreate,
    session: AsyncSession = Depends(get_session),
):
    name = platform_data.name.strip()
    slug = platform_data.slug.strip().lower()

    if not name or not slug:
        raise HTTPException(
            status_code=422,
            detail="Platform name and slug cannot be empty",
        )

    existing = await session.execute(
        select(Platform).where(
            Platform.slug == slug
        )
    )

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=409,
            detail="Platform slug already exists",
        )

    platform = Platform(
        name=name,
        slug=slug,
        description=platform_data.description,
    )

    session.add(platform)

    try:
        await session.commit()
        await session.refresh(platform)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Platform already exists",
        )

    return platform


# GET PLATFORM BY ID
@router.get(
    "/{platform_id}",
    response_model=PlatformRead,
)
async def get_platform(
    platform_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Platform).where(
            Platform.id == platform_id
        )
    )

    platform = result.scalar_one_or_none()

    if platform is None:
        raise HTTPException(
            status_code=404,
            detail="Platform not found",
        )

    return platform


# DELETE PLATFORM
@router.delete(
    "/{platform_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_platform(
    platform_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Platform).where(
            Platform.id == platform_id
        )
    )

    platform = result.scalar_one_or_none()

    if platform is None:
        raise HTTPException(
            status_code=404,
            detail="Platform not found",
        )

    await session.delete(platform)
    await session.commit()

    return None
