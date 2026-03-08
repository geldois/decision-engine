from dataclasses import dataclass
from uuid import UUID

from app.application.dto.decision_status import DecisionStatus

@dataclass(frozen = True)
class ProduceDecisionDtoResponse:
    event_id: UUID
    status: DecisionStatus
    