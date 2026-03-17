from dataclasses import dataclass
from uuid import UUID

from app.application.contracts.dto.dto_response import DtoResponse
from app.application.types.decision_result import DecisionResult


@dataclass(frozen=True)
class RegisterRuleDtoResponse(DtoResponse):
    name: str
    outcome: DecisionResult
    rule_id: UUID
