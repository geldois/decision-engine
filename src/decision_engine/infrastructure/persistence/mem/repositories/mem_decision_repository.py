from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.application.contracts.repository import (
    DecisionRepository,
)

if TYPE_CHECKING:
    from uuid import UUID

    from decision_engine.domain.entities.decision import Decision
    from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage


class MemDecisionRepository(DecisionRepository):
    def __init__(self, storage: MemStorage) -> None:
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
