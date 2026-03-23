from dataclasses import dataclass
from uuid import UUID

from app.domain.value_objects.decision_outcome import DecisionOutcome


@dataclass(frozen=True)
class DTORegisterRuleResponse:
    name: str
    outcome: DecisionOutcome
    rule_id: UUID
