from typing import Type, List, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.database.enums import TaskStatus
from .models import Base

from .models import Task, DailyLog, Goal, Setting, Note, OutreachSchedule
from datetime import date


class Database:
    def __init__(self, db_path: str = "athena.db") -> None:
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()

    def create_tables(self) -> None:
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.Session()


class Transactor:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, obj: Any) -> None:
        self.session.add(obj)
        self.session.commit()

    def get(self, model: Type[Any], obj_id: str) -> Optional[Any]:
        return self.session.query(model).get(obj_id)

    def get_all(self, model: Type[Any]) -> List[Any]:
        return self.session.query(model).all()

    def query(self, model: Type[Any], *criterion: Any) -> Any:
        return self.session.query(model).filter(*criterion)

    def delete(self, obj: Any) -> None:
        self.session.delete(obj)
        self.session.commit()


class TaskTransactor:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_todays_tasks(self) -> List[Any]:
        return self.session.query(Task).filter(Task.due_date == date.today()).all()

    def add_new_task_for_today(self, description: str, task_type: str) -> Task:
        new_task = Task(description=description, type=task_type, due_date=date.today())
        self.session.add(new_task)
        self.session.commit()
        return new_task

    def set_task_as_done(self, task: Task) -> None:
        task.status = TaskStatus.DONE
        self.session.commit()


class GoalTransactor:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_goal(self, description: str) -> Goal:
        new_goal = Goal(description=description)
        self.session.add(new_goal)
        self.session.commit()
        return new_goal

    def get_active_goals(self) -> List[Goal]:
        return self.session.query(Goal).filter(Goal.is_active).all()


class OutreachScheduleTransactor:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_next_outreach(self) -> Optional[OutreachSchedule]:
        return (
            self.session.query(OutreachSchedule)
            .order_by(OutreachSchedule.next_outreach)
            .first()
        )

    def add_outreach_schedule(self, next_outreach: date) -> OutreachSchedule:
        new_schedule = OutreachSchedule(ext_outreach_time=next_outreach)
        self.session.add(new_schedule)
        self.session.commit()
        return new_schedule
