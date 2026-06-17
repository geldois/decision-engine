from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.application.contracts.repository import (
    EventRepository,
)

if TYPE_CHECKING:
    from uuid import UUID

    from decision_engine.domain.entities.event import Event
    from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage


class MemEventRepository(EventRepository):
    def __init__(self, storage: MemStorage) -> None:
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
