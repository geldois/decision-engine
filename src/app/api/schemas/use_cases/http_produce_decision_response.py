from uuid import UUID

from pydantic import BaseModel


class HTTPProduceDecisionResponse(BaseModel):
    event_id: UUID
    rule_id: UUID | None
    status: str
    explanation: str
    decision_id: UUID
