from sqlalchemy import Column, DateTime, Integer, String, func

from db import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
