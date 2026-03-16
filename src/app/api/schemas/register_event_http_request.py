from typing import Any, Dict

from pydantic import BaseModel


class RegisterEventHttpRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any]
    timestamp: int
