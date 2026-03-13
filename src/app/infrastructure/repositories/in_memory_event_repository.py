from uuid import UUID

from app.domain.entities.events.event import Event
from app.application.repositories.event_repository_contract import EventRepositoryContract

class InMemoryEventRepository(EventRepositoryContract):
    # initializer
    def __init__(self):
        self._events = {}

    # methods

    # interface methods
    def save(
        self, 
        event: Event
    ) -> Event:
        self._events[event._id] = event

        return event
    
    def delete(
        self, 
        event: Event
    ) -> bool:
        if event._id in self._events:
            self._events.pop(event._id)

            return True
        
        return False
    
    def get_by_id(
        self, 
        event_id: UUID
    ) -> Event | None:
        return self._events.get(event_id, None)
    
    def list_all(self) -> list[Event]:
        return list(self._events.values())
    