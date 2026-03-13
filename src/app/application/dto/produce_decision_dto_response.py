from dataclasses import dataclass
from uuid import UUID

from app.application.types.decision_result import DecisionResult


@dataclass(frozen=True)
class ProduceDecisionDtoResponse:
    event_id: UUID
    rule_id: UUID | None
    status: DecisionResult
    explanation: str
    decision_id: UUID
