
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.session import get_session
from app.models.title import Title, Genre, Platform
from app.schemas.title import TitleCreate, TitleRead, TitleUpdate
from app.core.cache import cache_get, cache_set, cache_clear


router = APIRouter(
    prefix="/titles",
    tags=["Titles"],
)


def title_query():
    return (
        select(Title)
        .options(
            selectinload(Title.genres),
            selectinload(Title.platforms),
        )
    )


async def validate_genres(
    genre_ids: List[int],
    session: AsyncSession,
):
    if len(genre_ids) != len(set(genre_ids)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate genre IDs are not allowed",
        )

    if not genre_ids:
        return []

    result = await session.execute(
        select(Genre).where(Genre.id.in_(genre_ids))
    )

    genres = result.scalars().all()

    if len(genres) != len(genre_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more genre IDs are invalid",
        )

    return genres


async def validate_platforms(
    platform_ids: List[int],
    session: AsyncSession,
):
    if len(platform_ids) != len(set(platform_ids)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate platform IDs are not allowed",
        )

    if not platform_ids:
        return []

    result = await session.execute(
        select(Platform).where(
            Platform.id.in_(platform_ids)
        )
    )

    platforms = result.scalars().all()

    if len(platforms) != len(platform_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more platform IDs are invalid",
        )

    return platforms


# CREATE TITLE
@router.post(
    "/",
    response_model=TitleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_title(
    title_data: TitleCreate,
    session: AsyncSession = Depends(get_session),
):
    genres = await validate_genres(
        title_data.genre_ids,
        session,
    )

    platforms = await validate_platforms(
        title_data.platform_ids,
        session,
    )

    title = Title(
        title=title_data.title,
        original_title=title_data.original_title,
        description=title_data.description,
        release_year=title_data.release_year,
        rating=title_data.rating,
        duration_minutes=title_data.duration_minutes,
        is_featured=title_data.is_featured,
        genres=genres,
        platforms=platforms,
    )

    session.add(title)
    await session.commit()

    result = await session.execute(
        title_query().where(Title.id == title.id)
    )

    created_title = result.scalar_one()

    await cache_clear()

    return created_title


# GET ALL TITLES WITH FILTERING AND CACHING
@router.get(
    "/",
    response_model=List[TitleRead],
)
async def list_titles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    genre_id: Optional[int] = None,
    platform_id: Optional[int] = None,
    year: Optional[int] = Query(None, ge=1900, le=2100),
    search: Optional[str] = None,
    featured: Optional[bool] = None,
    session: AsyncSession = Depends(get_session),
):
    cache_key = (
        f"titles:{skip}:{limit}:{genre_id}:{platform_id}:"
        f"{year}:{search}:{featured}"
    )

    cached_data = await cache_get(cache_key)

    if cached_data is not None:
        return [
            TitleRead.model_validate(item)
            for item in cached_data
        ]

    query = title_query()

    if genre_id is not None:
        query = query.where(
            Title.genres.any(Genre.id == genre_id)
        )

    if platform_id is not None:
        query = query.where(
            Title.platforms.any(
                Platform.id == platform_id
            )
        )

    if year is not None:
        query = query.where(
            Title.release_year == year
        )

    if search:
        query = query.where(
            Title.title.ilike(f"%{search}%")
        )

    if featured is not None:
        query = query.where(
            Title.is_featured == featured
        )

    query = (
        query
        .order_by(Title.id)
        .offset(skip)
        .limit(limit)
    )

    result = await session.execute(query)
    titles = result.scalars().all()

    response_data = [
        TitleRead.model_validate(title).model_dump(mode="json")
        for title in titles
    ]

    await cache_set(
        cache_key,
        response_data,
        expiration=300,
    )

    return titles


# GET TITLE BY ID
@router.get(
    "/{title_id}",
    response_model=TitleRead,
)
async def get_title(
    title_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        title_query().where(Title.id == title_id)
    )

    title = result.scalar_one_or_none()

    if title is None:
        raise HTTPException(
            status_code=404,
            detail="Title not found",
        )

    return title


# UPDATE TITLE
@router.put(
    "/{title_id}",
    response_model=TitleRead,
)
async def update_title(
    title_id: int,
    title_data: TitleUpdate,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        title_query().where(Title.id == title_id)
    )

    title = result.scalar_one_or_none()

    if title is None:
        raise HTTPException(
            status_code=404,
            detail="Title not found",
        )

    update_data = title_data.model_dump(
        exclude_unset=True
    )

    if "genre_ids" in update_data:
        genres = await validate_genres(
            update_data.pop("genre_ids"),
            session,
        )
        title.genres = genres

    if "platform_ids" in update_data:
        platforms = await validate_platforms(
            update_data.pop("platform_ids"),
            session,
        )
        title.platforms = platforms

    for field, value in update_data.items():
        setattr(title, field, value)

    await session.commit()

    result = await session.execute(
        title_query().where(Title.id == title_id)
    )

    updated_title = result.scalar_one()

    await cache_clear()

    return updated_title


# DELETE TITLE
@router.delete(
    "/{title_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_title(
    title_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Title).where(
            Title.id == title_id
        )
    )

    title = result.scalar_one_or_none()

    if title is None:
        raise HTTPException(
            status_code=404,
            detail="Title not found",
        )

    await session.delete(title)
    await session.commit()

    await cache_clear()

    return None
