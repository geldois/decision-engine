from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID


@dataclass(frozen=True)
class RegisterEventDTOResponse:
    event_type: str
    payload: dict[str, object]
    occurred_at: int
    event_id: UUID
