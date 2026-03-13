from pydantic import BaseModel
from uuid import UUID

class ProduceDecisionHttpResponse(BaseModel):
    event_id: UUID
    rule_id: UUID | None
    status: str
    explanation: str
    decision_id: UUID
    