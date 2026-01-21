from abc import ABC, abstractmethod

from app.domain.events.event import Event

class EventRepository(ABC):
    @abstractmethod
    def save(
        self, 
        event: Event
    ) -> Event:
        ...