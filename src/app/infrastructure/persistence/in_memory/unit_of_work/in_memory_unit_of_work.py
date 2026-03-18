from copy import deepcopy
from typing import Callable

from app.application.contracts.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.application.contracts.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.application.contracts.repositories.rule_repository_contract import (
    RuleRepositoryContract,
)
from app.application.contracts.unit_of_works.unit_of_work_contract import (
    UnitOfWorkContract,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


class InMemoryUnitOfWork(UnitOfWorkContract):
    def __init__(
        self,
        in_memory_storage: InMemoryStorage,
        decision_repository_factory: Callable[
            [InMemoryStorage], DecisionRepositoryContract
        ],
        event_repository_factory: Callable[[InMemoryStorage], EventRepositoryContract],
        rule_repository_factory: Callable[[InMemoryStorage], RuleRepositoryContract],
    ):
        self.in_memory_storage = in_memory_storage
        self.decision_repository_factory = decision_repository_factory
        self.event_repository_factory = event_repository_factory
        self.rule_repository_factory = rule_repository_factory

    def __enter__(self) -> UnitOfWorkContract:
        self.in_memory_storage_copy = deepcopy(self.in_memory_storage)
        self.decision_repository = self.decision_repository_factory(
            self.in_memory_storage_copy
        )
        self.event_repository = self.event_repository_factory(
            self.in_memory_storage_copy
        )
        self.rule_repository = self.rule_repository_factory(self.in_memory_storage_copy)

        return super().__enter__()

    def commit(self) -> None:
        self.in_memory_storage.decisions.clear()
        self.in_memory_storage.decisions.update(
            deepcopy(self.in_memory_storage_copy.decisions)
        )
        self.in_memory_storage.events.clear()
        self.in_memory_storage.events.update(
            deepcopy(self.in_memory_storage_copy.events)
        )
        self.in_memory_storage.rules.clear()
        self.in_memory_storage.rules.update(deepcopy(self.in_memory_storage_copy.rules))
        
        del self.in_memory_storage_copy

    def rollback(self) -> None:
        del self.in_memory_storage_copy
