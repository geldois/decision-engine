from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class DTORegisterRuleResponse:
    name: str
    condition: dict[str, Any]
    outcome: str
    priority: int
    rule_id: UUID
