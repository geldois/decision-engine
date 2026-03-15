from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class RegisterEventDtoResponse:
    event_type: str
    payload: dict
    timestamp: int
    event_id: UUID
