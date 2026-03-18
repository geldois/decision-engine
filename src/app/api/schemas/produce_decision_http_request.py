from uuid import UUID

from app.api.contracts.schemas.http_contract import HttpContract


class ProduceDecisionHttpRequest(HttpContract):
    event_id: UUID
