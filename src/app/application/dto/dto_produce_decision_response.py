from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class DTOProduceDecisionResponse:
    event_id: UUID
    rule_id: UUID | None
    status: str
    traces: list[dict[str, Any]]
    decision_id: UUID
