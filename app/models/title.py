from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, ForeignKey, Text, Index
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base


class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    original_title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    release_year = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=True)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=True)

    genre = relationship("Genre", back_populates="titles")
    platform = relationship("Platform", back_populates="titles")

    __table_args__ = (
        Index("ix_titles_title", "title"),
        Index("ix_titles_release_year", "release_year"),
        Index("ix_titles_is_featured", "is_featured"),
    )


class TitleGenre(Base):
    __tablename__ = "title_genres"

    title_id = Column(Integer, ForeignKey("titles.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)