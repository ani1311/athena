"""Database enums for Athena models."""

from enum import Enum


class TaskStatus(str, Enum):
    """Task status options."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    """Task type options."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SOMETIME = "sometime"


class InteractionSender(str, Enum):
    """Interaction sender options."""

    USER = "user"
    AGENT = "agent"


class OutreachType(str, Enum):
    """Outreach schedule type options."""

    WAKEUP = "wakeup"
    SLEEP = "sleep"
    HOURLY = "hourly"
