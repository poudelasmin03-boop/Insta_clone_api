from database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from sqlalchemy.orm import relationship
from datetime import timedelta, timezone, datetime


class DbUser(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    create_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    items = relationship("DbPost", back_populates="user")


class DbPost(Base):
    __tablename__ = "Posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    content = Column(String, nullable=False)
    create_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    user_id = Column(Integer, ForeignKey("Users.id"))
    user = relationship("DbUser", back_populates="items")
