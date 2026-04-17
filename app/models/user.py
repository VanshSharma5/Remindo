from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    profession = Column(String)

    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    priority = Column(Integer)
    scheduled_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")