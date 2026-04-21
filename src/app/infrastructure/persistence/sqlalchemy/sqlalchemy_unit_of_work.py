from collections.abc import Callable

from sqlalchemy.orm import Session

from app.application.contracts.repository import (
    DecisionRepository,
    EventRepository,
    RuleRepository,
)
from app.application.contracts.unit_of_work import UnitOfWork
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_decision_repository import (
    SQLAlchemyDecisionRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_event_repository import (
    SQLAlchemyEventRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_rule_repository import (
    SQLAlchemyRuleRepository,
)


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        session_factory: Callable[[], Session],
        decision_repo_factory: Callable[
            [Session], DecisionRepository
        ] = SQLAlchemyDecisionRepository,
        event_repo_factory: Callable[
            [Session], EventRepository
        ] = SQLAlchemyEventRepository,
        rule_repo_factory: Callable[
            [Session], RuleRepository
        ] = SQLAlchemyRuleRepository,
    ) -> None:
        self.session_factory = session_factory
        self.decision_repo_factory = decision_repo_factory
        self.event_repo_factory = event_repo_factory
        self.rule_repo_factory = rule_repo_factory

    def __enter__(self) -> UnitOfWork:
        self.session = self.session_factory()

        self.decisions = self.decision_repo_factory(self.session)
        self.events = self.event_repo_factory(self.session)
        self.rules = self.rule_repo_factory(self.session)

        return super().__enter__()

    def commit(self) -> None:
        self.session.commit()
        self.session.close()

    def rollback(self) -> None:
        self.session.rollback()
        self.session.close()
