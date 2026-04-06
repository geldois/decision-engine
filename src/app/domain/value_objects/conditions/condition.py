from abc import ABC, abstractmethod

from app.domain.entities.event import Event


class Condition(ABC):
    @abstractmethod
    def evaluate(self, event: Event) -> bool:
        raise NotImplementedError()
