from __future__ import annotations

from collections.abc import Callable

from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage
from decision_engine.infrastructure.persistence.mem.mem_uow import MemUoW


class MemDB:
    def __init__(
        self,
        uow_factory: Callable[[], MemUoW],
        storage: MemStorage,
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


class MemDBBuilder:
    @staticmethod
    def create_storage() -> MemStorage:
        return MemStorage()

    @staticmethod
    def create_uow_factory(storage: MemStorage) -> Callable[[], MemUoW]:
        return lambda: MemUoW(storage=storage)

    @classmethod
    def build(cls) -> MemDB:
        storage = cls.create_storage()

        return MemDB(
            uow_factory=cls.create_uow_factory(storage=storage),
            storage=storage,
        )
