from pydantic import BaseModel
from uuid import UUID

class ProduceDecisionHttpRequest(BaseModel):
    event_id: UUID
    