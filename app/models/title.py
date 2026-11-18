
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


title_genres = Table(
    "title_genres",
    Base.metadata,
    Column(
        "title_id",
        Integer,
        ForeignKey("titles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "genre_id",
        Integer,
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


title_platforms = Table(
    "title_platforms",
    Base.metadata,
    Column(
        "title_id",
        Integer,
        ForeignKey("titles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "platform_id",
        Integer,
        ForeignKey("platforms.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    titles = relationship(
        "Title",
        secondary=title_genres,
        back_populates="genres",
    )


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    titles = relationship(
        "Title",
        secondary=title_platforms,
        back_populates="platforms",
    )


class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    original_title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    release_year = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    genres = relationship(
        "Genre",
        secondary=title_genres,
        back_populates="titles",
    )

    platforms = relationship(
        "Platform",
        secondary=title_platforms,
        back_populates="titles",
    )

    __table_args__ = (
        Index("ix_titles_title", "title"),
        Index("ix_titles_release_year", "release_year"),
        Index("ix_titles_is_featured", "is_featured"),
    )
