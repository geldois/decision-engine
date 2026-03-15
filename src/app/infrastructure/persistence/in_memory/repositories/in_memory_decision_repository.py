from uuid import UUID

from app.application.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.domain.entities.decisions.decision import Decision
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


class InMemoryDecisionRepository(DecisionRepositoryContract):
    def __init__(self, in_memory_storage: InMemoryStorage):
        self._decisions = in_memory_storage._decisions

    def save(self, decision: Decision) -> Decision:
        self._decisions[decision._id] = decision

        return decision

    def delete(self, decision: Decision) -> bool:
        if decision._id in self._decisions:
            self._decisions.pop(decision._id)

            return True

        return False

    def get_by_id(self, decision_id: UUID) -> Decision | None:
        return self._decisions.get(decision_id, None)

    def list_all(self) -> list[Decision]:
        return list(self._decisions.values())
