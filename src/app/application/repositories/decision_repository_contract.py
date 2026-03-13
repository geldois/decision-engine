from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.decisions.decision import Decision

class DecisionRepositoryContract(ABC):
    # interface methods
    @abstractmethod
    def save(
        self, 
        decision: Decision
    ) -> Decision:
        ...

    @abstractmethod
    def delete(
        self, 
        decision: Decision
    ) -> bool:
        ...

    @abstractmethod
    def get_by_id(
        self, 
        decision_id: UUID
    ) -> Decision | None:
        ...

    @abstractmethod
    def list_all(self) -> list[Decision]:
        ...
        