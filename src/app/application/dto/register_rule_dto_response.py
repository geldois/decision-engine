from dataclasses import dataclass
from uuid import UUID

from app.application.types.decision_result import DecisionResult

@dataclass(frozen = True)
class RegisterRuleDtoResponse:
    name: str
    outcome: DecisionResult
    rule_id: UUID
    