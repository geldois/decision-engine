from uuid import UUID

from pydantic import BaseModel


class HTTPProduceDecisionRequest(BaseModel):
    event_id: UUID
