from collections.abc import Callable

from sqlalchemy.orm import Session

from app.application.contracts.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.application.contracts.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.application.contracts.repositories.rule_repository_contract import (
    RuleRepositoryContract,
)
from app.application.contracts.unit_of_work_contract import (
    UnitOfWorkContract,
)


class SqlUnitOfWork(UnitOfWorkContract):
    def __init__(
        self,
        session_factory: Callable[[], Session],
        decision_repository_factory: Callable[[Session], DecisionRepositoryContract],
        event_repository_factory: Callable[[Session], EventRepositoryContract],
        rule_repository_factory: Callable[[Session], RuleRepositoryContract],
    ) -> None:
        self.session_factory = session_factory
        self.decision_repository_factory = decision_repository_factory
        self.event_repository_factory = event_repository_factory
        self.rule_repository_factory = rule_repository_factory

    def __enter__(self) -> UnitOfWorkContract:
        self.session = self.session_factory()
        self.decisions = self.decision_repository_factory(self.session)
        self.events = self.event_repository_factory(self.session)
        self.rules = self.rule_repository_factory(self.session)

        return super().__enter__()

    def commit(self) -> None:
        self.session.commit()
        self.session.close()

    def rollback(self) -> None:
        self.session.rollback()
        self.session.close()
