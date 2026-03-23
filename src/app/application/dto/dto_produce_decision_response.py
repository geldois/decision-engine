from dataclasses import dataclass
from uuid import UUID

from app.domain.value_objects.decision_outcome import DecisionOutcome


@dataclass(frozen=True)
class DTOProduceDecisionResponse:
    event_id: UUID
    rule_id: UUID | None
    status: DecisionOutcome
    explanation: str
    decision_id: UUID
