from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DTORegisterEventRequest:
    event_type: str
    payload: dict[str, Any]
    timestamp: int
