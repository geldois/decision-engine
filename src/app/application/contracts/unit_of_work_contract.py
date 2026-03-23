from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType

from app.application.contracts.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.application.contracts.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.application.contracts.repositories.rule_repository_contract import (
    RuleRepositoryContract,
)


class UnitOfWorkContract(ABC):
    decisions: DecisionRepositoryContract
    events: EventRepositoryContract
    rules: RuleRepositoryContract

    def __enter__(self) -> UnitOfWorkContract:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        exception_traceback: TracebackType | None,
    ):
        if exception_type:
            self.rollback()

            return False
        else:
            self.commit()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
