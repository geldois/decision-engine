from enum import Enum
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity


class EventField(Enum):
    EVENT_ID = "_id"
    EVENT_TYPE = "event_type"
    TIMESTAMP = "timestamp"


class Event(DomainEntity):
    __slots__ = ("_id", "event_type", "payload", "timestamp")

    def __init__(
        self,
        event_type: str,
        payload: dict,
        timestamp: int,
        event_id: UUID | None = None,
    ):

        if not event_type or not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("Event type is required.")

        if not payload:
            raise ValueError("Event payload is required.")

        if not timestamp or not isinstance(timestamp, int) or timestamp < 0:
            raise ValueError("Event timestamp is required.")

        if event_id and not isinstance(event_id, UUID):
            raise ValueError("Event ID is invalid.")

        self.event_type = event_type.strip()
        self.payload = payload
        self.timestamp = timestamp
        super().__init__(event_id)

    def get_field_value(self, event_field: EventField):
        return self.__getattribute__(event_field.value)
