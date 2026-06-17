from collections.abc import Callable

from decision_engine.application.contracts.repository import (
    DecisionRepository,
    EventRepository,
    RuleRepository,
)
from decision_engine.application.contracts.uow import UoW
from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage
from decision_engine.infrastructure.persistence.mem.repositories.mem_decision_repository import (
    MemDecisionRepository,
)
from decision_engine.infrastructure.persistence.mem.repositories.mem_event_repository import (
    MemEventRepository,
)
from decision_engine.infrastructure.persistence.mem.repositories.mem_rule_repository import (
    MemRuleRepository,
)


class MemUoW(UoW):
    def __init__(
        self,
        storage: MemStorage,
        decision_repo_factory: Callable[
            [MemStorage], DecisionRepository
        ] = MemDecisionRepository,
        event_repo_factory: Callable[
            [MemStorage], EventRepository
        ] = MemEventRepository,
        rule_repo_factory: Callable[
            [MemStorage], RuleRepository
        ] = MemRuleRepository,
    ) -> None:
        self.storage = storage
        self.decision_repo_factory = decision_repo_factory
        self.event_repo_factory = event_repo_factory
        self.rule_repo_factory = rule_repo_factory

    def __enter__(self) -> UoW:
        self.storage_backup = self.storage.backup()

        self.decisions = self.decision_repo_factory(self.storage_backup)
        self.events = self.event_repo_factory(self.storage_backup)
        self.rules = self.rule_repo_factory(self.storage_backup)

        return super().__enter__()

    def commit(self) -> None:
        self.storage.clear()
        self.storage.update(new_storage=self.storage_backup)

        del self.storage_backup

    def rollback(self) -> None:
        del self.storage_backup
