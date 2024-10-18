from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())


class User(Base, BaseMixin):
    __tablename__ = 'users'

    name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    telegram_id = Column(BigInteger, nullable=False, unique=True)

    tasks = relationship("Task", back_populates="owner")


class Task(Base, BaseMixin):
    __tablename__ = 'tasks'

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="tasks")
    is_done = Column(Boolean, default=False)
