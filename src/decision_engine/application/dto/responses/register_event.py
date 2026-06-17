from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True)
class RegisterEventDTOResponse:
    event_type: str
    payload: dict[str, Any]
    occurred_at: int
    event_id: UUID
