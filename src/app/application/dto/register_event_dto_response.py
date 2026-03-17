from dataclasses import dataclass
from typing import Any, Dict
from uuid import UUID

from app.application.contracts.dto.dto_response import DtoResponse


@dataclass(frozen=True)
class RegisterEventDtoResponse(DtoResponse):
    event_type: str
    payload: Dict[str, Any]
    timestamp: int
    event_id: UUID
