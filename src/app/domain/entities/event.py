from typing import Any
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity
from app.domain.exceptions.event_exception import EventException
from app.domain.value_objects.event_field import EventField


class Event(DomainEntity):
    def __init__(
        self,
        event_type: str,
        payload: dict[str, Any],
        timestamp: int,
        event_id: UUID | None = None,
    ) -> None:
        if not event_type.strip():
            raise EventException.event_type_cannot_be_empty(
                details={"event_type": event_type}
            )

        if not payload:
            raise EventException.event_payload_cannot_be_empty(
                details={"payload": payload}
            )

        if not timestamp:
            raise EventException.event_timestamp_cannot_be_zero(
                details={"timestamp": timestamp}
            )

        if timestamp < 0:
            raise EventException.event_timestamp_cannot_be_negative(
                details={"timestamp": timestamp}
            )

        self.event_type = event_type
        self.payload = payload
        self.timestamp = timestamp
        super().__init__(event_id)

    def get_field_value(self, event_field: EventField) -> str:
        return self.__getattribute__(event_field.value)
