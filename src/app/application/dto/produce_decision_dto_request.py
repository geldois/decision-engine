from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ProduceDecisionDtoRequest:
    event_id: UUID
