from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from decision_engine.application.protocols.unit_of_work_factory_protocol import (
        UoWProtocol,
    )


class DBProtocol(Protocol):
    @property
    def uow_factory(self) -> UoWProtocol: ...

    def check_health(self) -> bool: ...

    def clear_db(self) -> None: ...
