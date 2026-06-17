from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True)
class ProduceDecisionDTOResponse:
    event_id: UUID
    rule_id: UUID | None
    status: str
    traces: list[dict[str, object]]
    decision_id: UUID
