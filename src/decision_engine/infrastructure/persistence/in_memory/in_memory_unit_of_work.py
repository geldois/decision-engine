from collections.abc import Callable

from decision_engine.application.contracts.repository import (
    DecisionRepository,
    EventRepository,
    RuleRepository,
)
from decision_engine.application.contracts.uow import UoW
from decision_engine.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage
from decision_engine.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    InMemoryDecisionRepository,
)
from decision_engine.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from decision_engine.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
)


class InMemoryUnitOfWork(UoW):
    def __init__(
        self,
        storage: InMemoryStorage,
        decision_repo_factory: Callable[
            [InMemoryStorage], DecisionRepository
        ] = InMemoryDecisionRepository,
        event_repo_factory: Callable[
            [InMemoryStorage], EventRepository
        ] = InMemoryEventRepository,
        rule_repo_factory: Callable[
            [InMemoryStorage], RuleRepository
        ] = InMemoryRuleRepository,
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
