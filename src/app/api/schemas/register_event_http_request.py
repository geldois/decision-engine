from pydantic import BaseModel

class RegisterEventHttpRequest(BaseModel):
    event_type: str
    payload: dict
    timestamp: int
    