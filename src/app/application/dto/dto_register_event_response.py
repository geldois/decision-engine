from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class DTORegisterEventResponse:
    event_type: str
    payload: dict[str, Any]
    occurred_at: int
    event_id: UUID
