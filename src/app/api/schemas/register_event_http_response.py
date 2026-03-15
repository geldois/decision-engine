from uuid import UUID

from pydantic import BaseModel


class RegisterEventHttpResponse(BaseModel):
    event_type: str
    payload: dict
    timestamp: int
    event_id: UUID
