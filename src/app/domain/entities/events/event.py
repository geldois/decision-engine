from enum import Enum
from typing import Any
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity


class ExposibleEventField(Enum):
    EVENT_ID = "id"
    EVENT_TYPE = "event_type"
    TIMESTAMP = "timestamp"


class Event(DomainEntity):
    def __init__(
        self,
        event_type: str,
        payload: dict[str, Any],
        timestamp: int,
        event_id: UUID | None = None,
    ) -> None:

        if not event_type.strip():
            raise ValueError("invalid event_type")

        if not payload:
            raise ValueError("invalid event payload")

        if not timestamp or timestamp < 0:
            raise ValueError("invalid event timestamp")

        self.event_type = event_type.strip()
        self.payload = payload
        self.timestamp = timestamp
        super().__init__(event_id)

    def get_field_value(self, exposible_event_field: ExposibleEventField) -> str:
        return self.__getattribute__(exposible_event_field.value)
