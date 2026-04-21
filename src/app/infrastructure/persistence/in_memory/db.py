from collections.abc import Callable

from app.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage
from app.infrastructure.persistence.in_memory.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    InMemoryDecisionRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
)


class InMemoryDB:
    def __init__(
        self,
        uow_factory: Callable[[], InMemoryUnitOfWork],
        storage: InMemoryStorage,
    ) -> None:
        self.uow_factory = uow_factory
        self.storage = storage

    def check_health(self) -> bool:
        return True

    def clear_db(self) -> None:
        try:
            self.storage.clear()
        except Exception as exception:
            raise exception


class InMemoryDBBuilder:
    @staticmethod
    def create_storage() -> InMemoryStorage:
        return InMemoryStorage()

    @staticmethod
    def create_uow_factory(
        storage: InMemoryStorage,
    ) -> Callable[[], InMemoryUnitOfWork]:
        return lambda: InMemoryUnitOfWork(
            storage=storage,
            decision_repo_factory=InMemoryDecisionRepository,
            event_repo_factory=InMemoryEventRepository,
            rule_repo_factory=InMemoryRuleRepository,
        )

    @classmethod
    def build(cls) -> InMemoryDB:
        storage = cls.create_storage()

        return InMemoryDB(
            uow_factory=cls.create_uow_factory(storage=storage),
            storage=storage,
        )
