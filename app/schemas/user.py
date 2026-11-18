from ..database.base import Base
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UserCreate(UserBase):
    pass

class UserRead(BaseModel):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None, max_length=255)