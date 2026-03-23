from typing import Any
from uuid import UUID

from pydantic import BaseModel


class HTTPRegisterEventResponse(BaseModel):
    event_type: str
    payload: dict[str, Any]
    timestamp: int
    event_id: UUID
