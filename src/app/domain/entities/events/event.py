from typing import Any
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity
from app.domain.exceptions.events.event_exception import EventException
from app.domain.value_objects.exponible_event_field import ExponibleEventField


class Event(DomainEntity):
    def __init__(
        self,
        event_type: str,
        payload: dict[str, Any],
        timestamp: int,
        event_id: UUID | None = None,
    ) -> None:

        if not event_type.strip():
            raise EventException.event_type_cannot_be_empty()

        if not payload:
            raise EventException.event_payload_cannot_be_empty()

        if not timestamp:
            raise EventException.event_timestamp_cannot_be_zero(timestamp=timestamp)

        if timestamp < 0:
            raise EventException.event_timestamp_cannot_be_negative(timestamp=timestamp)

        self.event_type = event_type.strip()
        self.payload = payload
        self.timestamp = timestamp
        super().__init__(event_id)

    def get_field_value(self, exposible_event_field: ExponibleEventField) -> str:
        return self.__getattribute__(exposible_event_field.value)
