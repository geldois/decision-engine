from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class RegisterEventDtoRequest:
    event_type: str
    payload: Dict[str, Any]
    timestamp = int
