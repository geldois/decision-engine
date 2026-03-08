from pydantic import BaseModel

class ProduceDecisionHttpRequest(BaseModel):
    event_type: str
    payload: dict
    timestamp: int
    