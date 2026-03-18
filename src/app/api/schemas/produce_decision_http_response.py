from uuid import UUID

from app.api.contracts.schemas.http_contract import HttpContract


class ProduceDecisionHttpResponse(HttpContract):
    event_id: UUID
    rule_id: UUID | None
    status: str
    explanation: str
    decision_id: UUID
