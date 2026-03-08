from dataclasses import dataclass
from uuid import UUID

from app.domain.decisions.decision_outcome import DecisionOutcome

@dataclass(frozen = True)
class RegisterRuleDtoResponse:
    rule_id: UUID
    outcome: DecisionOutcome
    