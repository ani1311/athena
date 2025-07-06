from typing import Type, List, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base


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
