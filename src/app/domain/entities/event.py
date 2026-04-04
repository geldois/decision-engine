from datetime import datetime
from typing import Any
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity
from app.domain.exceptions.event_exception import EventException


class Event(DomainEntity):
    def __init__(
        self,
        event_type: str,
        payload: dict[str, Any],
        occurred_at: int,
        created_at: datetime | None = None,
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

        if not occurred_at:
            raise EventException.event_occurred_at_cannot_be_zero(
                details={"occurred_at": occurred_at}
            )

        if occurred_at < 0:
            raise EventException.event_occurred_at_cannot_be_negative(
                details={"occurred_at": occurred_at}
            )

        self.event_type = event_type
        self.payload = payload
        self.occurred_at = occurred_at
        super().__init__(created_at=created_at, entity_id=event_id)

    def is_structurally_equal(self, other: DomainEntity) -> bool:
        if not isinstance(other, Event):
            return False

        return (
            self.event_type == other.event_type
            and self.payload == other.payload
            and self.occurred_at == other.occurred_at
            and self.created_at == other.created_at
        )
