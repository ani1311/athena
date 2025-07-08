"""Database models for Athena."""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Boolean,
    Text,
    text,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

from .enums import TaskStatus, TaskType, InteractionSender, OutreachType

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    status = Column(
        Enum(TaskStatus), nullable=False, default=TaskStatus.TODO
    )  # todo, in_progress, done, cancelled
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    type = Column(
        Enum(TaskType), nullable=False
    )  # "daily", "weekly", "monthly", "sometime"
    completed_at = Column(DateTime)
    due_date = Column(Date)
    is_sometime_task = Column(Boolean, nullable=False, default=False)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True)

    # Relationship
    goal = relationship("Goal", back_populates="tasks")


class DailyLog(Base):
    __tablename__ = "daily_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, unique=True)
    summary = Column(Text)


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationship
    tasks = relationship("Task", back_populates="goal")


class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(String)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(Enum(InteractionSender), nullable=False)  # "user" or "agent"
    content = Column(Text, nullable=False)
    timestamp = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class OutreachSchedule(Base):
    __tablename__ = "outreach_schedule"
    id = Column(Integer, primary_key=True, autoincrement=True)
    next_outreach_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    description = Column(Text, nullable=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
