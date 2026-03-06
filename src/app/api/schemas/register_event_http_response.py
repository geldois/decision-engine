from pydantic import BaseModel

class RegisterEventHttpResponse(BaseModel):
    event_id: int
    status: str
    