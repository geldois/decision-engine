from dataclasses import dataclass
from typing import Any, Dict
from uuid import UUID


@dataclass(frozen=True)
class RegisterEventDtoResponse:
    event_type: str
    payload: Dict[str, Any]
    timestamp: int
    event_id: UUID
