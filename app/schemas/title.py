
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# -------------------------
# GENRE SCHEMAS
# -------------------------

class GenreBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class GenreCreate(GenreBase):
    pass


class GenreRead(GenreBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# PLATFORM SCHEMAS
# -------------------------

class PlatformBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)


class PlatformCreate(PlatformBase):
    pass


class PlatformRead(PlatformBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# TITLE SCHEMAS
# -------------------------

class TitleBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    original_title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    release_year: Optional[int] = Field(default=None, ge=1900, le=2100)
    rating: Optional[float] = Field(default=None, ge=0, le=10)
    duration_minutes: Optional[int] = Field(default=None, ge=1)
    is_featured: bool = False

    genre_ids: List[int] = Field(default_factory=list)
    platform_ids: List[int] = Field(default_factory=list)


class TitleCreate(TitleBase):
    pass


class TitleRead(BaseModel):
    id: int
    title: str
    original_title: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    rating: Optional[float] = None
    duration_minutes: Optional[int] = None
    is_featured: bool = False

    genres: List[GenreRead] = Field(default_factory=list)
    platforms: List[PlatformRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class TitleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    original_title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    release_year: Optional[int] = Field(default=None, ge=1900, le=2100)
    rating: Optional[float] = Field(default=None, ge=0, le=10)
    duration_minutes: Optional[int] = Field(default=None, ge=1)
    is_featured: Optional[bool] = None

    # None means leave existing relationships unchanged.
    # An empty list means remove all relationships.
    genre_ids: Optional[List[int]] = None
    platform_ids: Optional[List[int]] = None
