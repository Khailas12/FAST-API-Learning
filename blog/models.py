from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func


class Blog(Base):
    __tablename__ = "blogs"
     
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None)
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=None)