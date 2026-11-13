from ..database.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, UniqueConstraint
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uix_email"),)
    
    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(255), nullable=False, unique=True)
    hashed_password: str = Column(String(255), nullable=False)
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)