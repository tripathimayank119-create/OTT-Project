from ..database.base import Base
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from pydantic import Field

class GenreBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

class GenreCreate(GenreBase):
    pass

class GenreRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PlatformBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

class PlatformCreate(PlatformBase):
    pass

class PlatformRead(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TitleBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    original_title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)
    release_year: Optional[int] = Field(default=None, ge=1900, le=2100)
    rating: Optional[float] = Field(default=None, ge=0, le=10)
    duration_minutes: Optional[int] = Field(default=None, ge=1)
    is_featured: bool = Field(default=False)
    genre_ids: List[int] = Field(default_factory=list, alias="genre_ids")
    platform_ids: List[int] = Field(default_factory=list, alias="platform_ids")

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
    genre: Optional[GenreRead] = None
    platform: Optional[PlatformRead] = None
    
    model_config = ConfigDict(from_attributes=True)

class TitleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    original_title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None)
    release_year: Optional[int] = Field(default=None, ge=1900, le=2100)
    rating: Optional[float] = Field(default=None, ge=0, le=10)
    duration_minutes: Optional[int] = Field(default=None, ge=1)
    is_featured: Optional[bool] = Field(default=None)
    genre_ids: List[int] = Field(default_factory=list, alias="genre_ids")
    platform_ids: List[int] = Field(default_factory=list, alias="platform_ids")