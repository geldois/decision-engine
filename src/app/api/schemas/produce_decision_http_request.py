from uuid import UUID

from pydantic import BaseModel


class ProduceDecisionHttpRequest(BaseModel):
    event_id: UUID
