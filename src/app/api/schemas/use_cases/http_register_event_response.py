from typing import Any
from uuid import UUID

from pydantic import BaseModel


class HTTPRegisterEventResponse(BaseModel):
    event_type: str
    payload: dict[str, Any]
    occurred_at: int
    event_id: UUID
