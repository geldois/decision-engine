from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DTOProduceDecisionResponse:
    event_id: UUID
    rule_id: UUID | None
    status: str
    explanation: str
    decision_id: UUID
