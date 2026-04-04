from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
from uuid import UUID, uuid4


class DomainEntity(ABC):
    def __init__(self, created_at: datetime | None, entity_id: UUID | None) -> None:
        if created_at is None:
            self.created_at = datetime.now(UTC)
        elif created_at.tzinfo is None:
            self.created_at = created_at.replace(tzinfo=UTC)
        else:
            self.created_at = created_at

        self.id = entity_id if entity_id else uuid4()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id

    @abstractmethod
    def is_structurally_equal(self, other: DomainEntity) -> bool:
        raise NotImplementedError()
