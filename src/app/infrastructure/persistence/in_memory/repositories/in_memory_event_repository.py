from uuid import UUID

from app.application.contracts.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.domain.entities.events.event import Event
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


class InMemoryEventRepository(EventRepositoryContract):
    def __init__(self, in_memory_storage: InMemoryStorage):
        self._events = in_memory_storage.events

    def save(self, event: Event) -> Event:
        self._events[event.id] = event

        return event

    def delete(self, event: Event) -> bool:
        if event.id in self._events:
            self._events.pop(event.id)

            return True

        return False

    def get_by_id(self, event_id: UUID) -> Event | None:
        return self._events.get(event_id, None)

    def list_all(self) -> list[Event]:
        return list(self._events.values())
