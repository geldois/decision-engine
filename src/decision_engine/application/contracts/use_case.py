from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from decision_engine.application.contracts.uow import UoW


class UseCase[Request, Response](ABC):
    def __init__(self, uow_factory: Callable[[], UoW]) -> None:
        self.uow_factory = uow_factory

    @abstractmethod
    def execute(self, dto: Request) -> Response:
        raise NotImplementedError
