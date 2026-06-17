from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import TracebackType

    from decision_engine.application.contracts.repository import (
        DecisionRepository,
        EventRepository,
        RuleRepository,
    )


class UoW(ABC):
    decisions: DecisionRepository
    events: EventRepository
    rules: RuleRepository

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        exception_traceback: TracebackType | None,
    ) -> None:
        if exception_type is None:
            self.commit()

            return

        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


type UoWFactory = Callable[[], UoW]
