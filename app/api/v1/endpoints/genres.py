
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.models.title import Genre
from app.schemas.title import GenreCreate, GenreRead


router = APIRouter(
    prefix="/genres",
    tags=["Genres"],
)


# GET ALL GENRES
@router.get(
    "/",
    response_model=List[GenreRead],
)
async def list_genres(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Genre).order_by(Genre.name)
    )

    return result.scalars().all()


# CREATE GENRE
@router.post(
    "/",
    response_model=GenreRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_genre(
    genre_data: GenreCreate,
    session: AsyncSession = Depends(get_session),
):
    name = genre_data.name.strip()

    if not name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Genre name cannot be empty",
        )

    existing = await session.execute(
        select(Genre).where(
            Genre.name.ilike(name)
        )
    )

    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genre already exists",
        )

    genre = Genre(
        name=name,
        description=genre_data.description,
    )

    session.add(genre)

    try:
        await session.commit()
        await session.refresh(genre)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Genre already exists",
        )

    return genre


# GET GENRE BY ID
@router.get(
    "/{genre_id}",
    response_model=GenreRead,
)
async def get_genre(
    genre_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Genre).where(
            Genre.id == genre_id
        )
    )

    genre = result.scalar_one_or_none()

    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found",
        )

    return genre


# DELETE GENRE
@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_genre(
    genre_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Genre).where(
            Genre.id == genre_id
        )
    )

    genre = result.scalar_one_or_none()

    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found",
        )

    await session.delete(genre)
    await session.commit()

    return None
