from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterEventDTORequest:
    event_type: str
    payload: dict[str, object]
    occurred_at: int
