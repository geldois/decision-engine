from dataclasses import dataclass

from app.application.dto.dto_condition import DTOCondition


@dataclass(frozen=True)
class DTORegisterRuleRequest:
    name: str
    condition: DTOCondition
    outcome: str
    priority: int
