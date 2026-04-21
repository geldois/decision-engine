from typing import Protocol

from app.application.contracts.unit_of_work import UnitOfWork


class UnitOfWorkFactoryProtocol(Protocol):
    def __call__(self) -> UnitOfWork: ...
