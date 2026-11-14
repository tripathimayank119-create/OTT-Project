from ..database.base import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional

class Genre(Base):
    __tablename__ = "genres"
    
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False, unique=True)
    description: Optional[str] = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_genres_name", "name"),
    )

class Platform(Base):
    __tablename__ = "platforms"
    
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False, unique=True)
    slug: str = Column(String(100), nullable=False, unique=True)
    description: Optional[str] = Column(Text, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_platforms_slug", "slug"),
    )

class Title(Base):
    __tablename__ = "titles"
    
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(255), nullable=False)
    original_title: Optional[str] = Column(String(255), nullable=True)
    description: Optional[str] = Column(Text, nullable=True)
    release_year: Optional[int] = Column(Integer, nullable=True)
    rating: Optional[float] = Column(Float, nullable=True)
    duration_minutes: Optional[int] = Column(Integer, nullable=True)
    is_featured: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    genre_id: int = Column(Integer, ForeignKey("genres.id"), nullable=True)
    platform_id: int = Column(Integer, ForeignKey("platforms.id"), nullable=True)
    
    genre = relationship("Genre", back_populates="titles")
    platform = relationship("Platform", back_populates="titles")
    
    __table_args__ = (
        Index("ix_titles_title", "title"),
        Index("ix_titles_release_year", "release_year"),
        Index("ix_titles_is_featured", "is_featured"),
    )

class TitleGenre(Base):
    __tablename__ = "title_genres"
    
    title_id: int = Column(Integer, ForeignKey("titles.id"), primary_key=True)
    genre_id: int = Column(Integer, ForeignKey("genres.id"), primary_key=True)