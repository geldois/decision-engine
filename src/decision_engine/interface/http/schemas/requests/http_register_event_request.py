from typing import Any

from pydantic import BaseModel


class HTTPRegisterEventRequest(BaseModel):
    event_type: str
    payload: dict[str, Any]
    occurred_at: int
