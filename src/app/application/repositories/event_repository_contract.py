from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.events.event import Event

class EventRepositoryContract(ABC):
    # interface methods
    @abstractmethod
    def save(
        self, 
        event: Event
    ) -> Event:
        ...
        
    @abstractmethod
    def delete(
        self, 
        event: Event
    ) -> bool:
        ...
    
    @abstractmethod
    def get_by_id(
        self, 
        event_id: UUID
    ) -> Event | None:
        ...

    @abstractmethod
    def list_all(self) -> list[Event]:
        ...
