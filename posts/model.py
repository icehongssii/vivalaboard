from sqlalchemy import  Column, Integer, String,DateTime, func,ForeignKey, Text
from db import Base

class Post(Base):
    __tablename__ = "POSTS"
    post_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    views = Column(Integer, default=0)

