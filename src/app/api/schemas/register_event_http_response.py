from typing import Any, Dict
from uuid import UUID

from app.api.contracts.schemas.http_contract import HttpContract


class RegisterEventHttpResponse(HttpContract):
    event_type: str
    payload: Dict[str, Any]
    timestamp: int
    event_id: UUID
