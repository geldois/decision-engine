from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.events.event import Event


class EventRepositoryContract(ABC):
    @abstractmethod
    def save(self, event: Event) -> Event:
        raise NotImplementedError

    @abstractmethod
    def delete(self, event: Event) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, event_id: UUID) -> Event | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Event]:
        raise NotImplementedError
