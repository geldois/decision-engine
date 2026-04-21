from typing import Protocol

from app.application.protocols.unit_of_work_factory_protocol import (
    UnitOfWorkFactoryProtocol,
)


class DBProtocol(Protocol):
    @property
    def uow_factory(self) -> UnitOfWorkFactoryProtocol: ...

    def check_health(self) -> bool: ...

    def clear_db(self) -> None: ...
