from abc import ABC, abstractmethod

from app.domain.events.event import Event

class EventRepositoryContract(ABC):
    @abstractmethod
    def save(
        self, 
        event: Event
    ) -> Event:
        ...