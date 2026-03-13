from pydantic import BaseModel
from uuid import UUID

class RegisterEventHttpRequest(BaseModel):
    event_type: str
    payload: dict
    timestamp: int
        