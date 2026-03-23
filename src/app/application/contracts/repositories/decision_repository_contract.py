from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.decision import Decision


class DecisionRepositoryContract(ABC):
    @abstractmethod
    def save(self, decision: Decision) -> Decision:
        raise NotImplementedError

    @abstractmethod
    def delete(self, decision: Decision) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, decision_id: UUID) -> Decision | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Decision]:
        raise NotImplementedError
