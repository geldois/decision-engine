from dataclasses import dataclass
from app.application.dto.decision_status import DecisionStatus

@dataclass(frozen = True)
class RegisterEventResponse:
    event_id: str
    status: DecisionStatus
    