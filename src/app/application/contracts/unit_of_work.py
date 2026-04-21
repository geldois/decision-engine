from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType

from app.application.contracts.repository import (
    DecisionRepository,
    EventRepository,
    RuleRepository,
)


class UnitOfWork(ABC):
    decisions: DecisionRepository
    events: EventRepository
    rules: RuleRepository

    def __enter__(self) -> UnitOfWork:
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
        raise NotImplementedError()

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError()
