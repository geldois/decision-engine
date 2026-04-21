from abc import ABC, abstractmethod
from collections.abc import Callable

from app.application.contracts.unit_of_work import UnitOfWork


class UseCase[Request, Response](ABC):
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self.uow_factory = uow_factory

    @abstractmethod
    def execute(self, dto: Request) -> Response:
        raise NotImplementedError()
