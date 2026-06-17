from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from decision_engine.application.contracts.uow import UoWFactory


class DBProtocol(Protocol):
    @property
    def uow_factory(self) -> UoWFactory: ...

    def check_health(self) -> bool: ...

    def clear_db(self) -> None: ...
