from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule


class DecisionRepository(ABC):
    @abstractmethod
    def save(self, decision: Decision) -> Decision:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, decision: Decision) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, decision_id: UUID) -> Decision | None:
        raise NotImplementedError()

    @abstractmethod
    def list_all(self) -> list[Decision]:
        raise NotImplementedError()


class EventRepository(ABC):
    @abstractmethod
    def save(self, event: Event) -> Event:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, event: Event) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, event_id: UUID) -> Event | None:
        raise NotImplementedError()

    @abstractmethod
    def list_all(self) -> list[Event]:
        raise NotImplementedError()


class RuleRepository(ABC):
    @abstractmethod
    def save(self, rule: Rule) -> Rule:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, rule: Rule) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, rule_id: UUID) -> Rule | None:
        raise NotImplementedError()

    @abstractmethod
    def list_all(self) -> list[Rule]:
        raise NotImplementedError()
