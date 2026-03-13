from pydantic import BaseModel
from uuid import UUID

class RegisterEventHttpResponse(BaseModel):
    event_type: str
    payload: dict
    timestamp: int
    event_id: UUID
