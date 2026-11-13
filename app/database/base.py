from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

@as_declarative()
class Base:
    pass