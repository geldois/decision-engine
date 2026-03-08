from abc import ABC, abstractmethod

from app.domain.decisions.decision import Decision

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
        decision_id: int
    ) -> Decision | None:
        ...

    @abstractmethod
    def list_all(self) -> list[Decision]:
        ...
        