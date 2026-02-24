from pydantic import BaseModel

class RegisterEventHttpResponse(BaseModel):
    event_id: str
    status: str
    