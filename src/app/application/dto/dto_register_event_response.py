from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class DTORegisterEventResponse:
    event_type: str
    payload: dict[str, Any]
    timestamp: int
    event_id: UUID
