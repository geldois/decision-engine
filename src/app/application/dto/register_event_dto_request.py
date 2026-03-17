from typing import Any, Dict

from app.application.contracts.dto.dto_request import DtoRequest


class RegisterEventDtoRequest(DtoRequest):
    __slots__ = ("event_type", "payload", "timestamp")

    def __init__(self, event_type: str, payload: Dict[str, Any], timestamp: int):
        self.event_type = event_type
        self.payload = payload
        self.timestamp = timestamp
