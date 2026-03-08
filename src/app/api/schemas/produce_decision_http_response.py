from pydantic import BaseModel
from uuid import UUID

class ProduceDecisionHttpResponse(BaseModel):
    event_id: UUID
    status: str
    