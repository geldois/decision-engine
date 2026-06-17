from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from decision_engine.application.dto.condition import ConditionDTO


@dataclass(frozen=True)
class RegisterRuleDTORequest:
    name: str
    condition: ConditionDTO
    outcome: str
    priority: int
