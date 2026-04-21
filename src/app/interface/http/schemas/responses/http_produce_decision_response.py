from typing import Any
from uuid import UUID

from pydantic import BaseModel


class HTTPProduceDecisionResponse(BaseModel):
    event_id: UUID
    rule_id: UUID | None
    status: str
    traces: list[dict[str, Any]]
    decision_id: UUID
