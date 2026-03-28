from typing import Any

from pydantic import BaseModel


class RegisterEventHttpRequest(BaseModel):
    event_type: str
    payload: dict[str, Any]
    timestamp: int
