from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Boolean
from db import Base


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    token_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    token = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    revoked = Column(Boolean, default=False)
