from uuid import UUID

from pydantic import BaseModel


class HTTPProduceDecisionResponse(BaseModel):
    event_id: UUID
    rule_id: UUID | None
    status: str
    traces: list[dict[str, object]]
    decision_id: UUID
