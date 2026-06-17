from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True)
class RegisterRuleDTOResponse:
    name: str
    condition: dict[str, Any]
    outcome: str
    priority: int
    rule_id: UUID
