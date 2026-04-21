from uuid import UUID

from app.application.contracts.repository import (
    EventRepository,
)
from app.domain.entities.event import Event
from app.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage


class InMemoryEventRepository(EventRepository):
    def __init__(self, storage: InMemoryStorage) -> None:
        self.events = storage.events

    def save(self, event: Event) -> Event:
        self.events[event.id] = event

        return event

    def delete(self, event: Event) -> bool:
        if event.id in self.events:
            self.events.pop(event.id)

            return True

        return False

    def get_by_id(self, event_id: UUID) -> Event | None:
        return self.events.get(event_id, None)

    def list_all(self) -> list[Event]:
        return list(self.events.values())
