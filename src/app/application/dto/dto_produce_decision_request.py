from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class DTOProduceDecisionRequest:
    event_id: UUID
