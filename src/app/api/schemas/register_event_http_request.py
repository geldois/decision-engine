from typing import Any, Dict

from app.api.contracts.schemas.http_contract import HttpContract


class RegisterEventHttpRequest(HttpContract):
    event_type: str
    payload: Dict[str, Any]
    timestamp: int
