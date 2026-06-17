from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from decision_engine.application.contracts.uow import UoWFactory


class UseCase[Request, Response](ABC):
    def __init__(self, uow_factory: UoWFactory) -> None:
        self.uow_factory = uow_factory

    @abstractmethod
    def execute(self, dto: Request) -> Response:
        raise NotImplementedError
