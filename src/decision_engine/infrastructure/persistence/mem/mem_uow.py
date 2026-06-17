from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.application.contracts.uow import UoW
from decision_engine.infrastructure.persistence.mem.repositories.mem_decision_repository import (  # noqa: E501
    MemDecisionRepository,
)
from decision_engine.infrastructure.persistence.mem.repositories.mem_event_repository import (  # noqa: E501
    MemEventRepository,
)
from decision_engine.infrastructure.persistence.mem.repositories.mem_rule_repository import (  # noqa: E501
    MemRuleRepository,
)

if TYPE_CHECKING:
    from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage


class MemUoW(UoW):
    def __init__(self, *, storage: MemStorage) -> None:
        self.storage = storage

    def __enter__(self) -> UoW:
        self.storage_backup = self.storage.backup()

        self.decisions = MemDecisionRepository(storage=self.storage_backup)
        self.events = MemEventRepository(storage=self.storage_backup)
        self.rules = MemRuleRepository(storage=self.storage_backup)

        return super().__enter__()

    def commit(self) -> None:
        self.storage.clear()
        self.storage.update(new_storage=self.storage_backup)

        del self.storage_backup

    def rollback(self) -> None:
        del self.storage_backup
