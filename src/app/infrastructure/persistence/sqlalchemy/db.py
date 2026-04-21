from collections.abc import Callable

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import Settings
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_decision_repository import (
    SQLAlchemyDecisionRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_event_repository import (
    SQLAlchemyEventRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_rule_repository import (
    SQLAlchemyRuleRepository,
)
from app.infrastructure.persistence.sqlalchemy.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)


class SQLAlchemyDB:
    def __init__(
        self,
        uow_factory: Callable[[], SQLAlchemyUnitOfWork],
        database_url: str,
        engine: Engine,
        session_factory: Callable[[], Session],
    ) -> None:
        self.uow_factory = uow_factory
        self.database_url = database_url
        self.engine = engine
        self.session_factory = session_factory

    def check_health(self) -> bool:
        try:
            with self.session_factory() as session:
                session.execute(text("SELECT 1"))

            return True
        except Exception:
            return False

    def clear_db(self) -> None:
        with self.session_factory() as session:
            try:
                session.execute(text("TRUNCATE TABLE decisions CASCADE"))
                session.execute(text("TRUNCATE TABLE events CASCADE"))
                session.execute(text("TRUNCATE TABLE rules CASCADE"))

                session.commit()
            except Exception as exception:
                session.rollback()

                raise exception


class SQLAlchemyDBBuilder:
    @staticmethod
    def create_engine_from_url(database_url: str) -> Engine:
        return create_engine(url=database_url, echo=True)

    @staticmethod
    def create_session_factory(engine: Engine) -> Callable[[], Session]:
        return sessionmaker(bind=engine)

    @staticmethod
    def create_uow_factory(
        session_factory: Callable[[], Session],
    ) -> Callable[[], SQLAlchemyUnitOfWork]:
        return lambda: SQLAlchemyUnitOfWork(
            session_factory=session_factory,
            decision_repo_factory=SQLAlchemyDecisionRepository,
            event_repo_factory=SQLAlchemyEventRepository,
            rule_repo_factory=SQLAlchemyRuleRepository,
        )

    @classmethod
    def build(cls, settings: Settings) -> SQLAlchemyDB:
        database_url = settings.database_url
        engine = cls.create_engine_from_url(database_url=database_url)
        session_factory = cls.create_session_factory(engine=engine)

        return SQLAlchemyDB(
            uow_factory=cls.create_uow_factory(session_factory=session_factory),
            database_url=database_url,
            engine=engine,
            session_factory=session_factory,
        )
