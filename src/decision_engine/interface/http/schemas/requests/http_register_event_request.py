from pydantic import BaseModel


class HTTPRegisterEventRequest(BaseModel):
    event_type: str
    payload: dict[str, object]
    occurred_at: int
