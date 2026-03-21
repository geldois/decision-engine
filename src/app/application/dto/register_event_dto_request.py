from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RegisterEventDtoRequest:
    event_type: str
    payload: dict[str, Any]
    timestamp: int
