from uuid import UUID

from app.application.contracts.repository import (
    DecisionRepository,
)
from app.domain.entities.decision import Decision
from app.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage


class InMemoryDecisionRepository(DecisionRepository):
    def __init__(self, storage: InMemoryStorage) -> None:
        self.decisions = storage.decisions

    def save(self, decision: Decision) -> Decision:
        self.decisions[decision.id] = decision

        return decision

    def delete(self, decision: Decision) -> bool:
        if decision.id in self.decisions:
            self.decisions.pop(decision.id)

            return True

        return False

    def get_by_id(self, decision_id: UUID) -> Decision | None:
        return self.decisions.get(decision_id, None)

    def list_all(self) -> list[Decision]:
        return list(self.decisions.values())
