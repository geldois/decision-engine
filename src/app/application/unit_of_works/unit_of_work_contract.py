from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType

from app.application.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.application.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.application.repositories.rule_repository_contract import RuleRepositoryContract


class UnitOfWorkContract(ABC):
    decision_repository: DecisionRepositoryContract
    event_repository: EventRepositoryContract
    rule_repository: RuleRepositoryContract

    def __enter__(self) -> UnitOfWorkContract:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
