from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel


class RegisterEventHttpResponse(BaseModel):
    event_type: str
    payload: Dict[str, Any]
    timestamp: int
    event_id: UUID
