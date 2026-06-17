from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from decision_engine.domain.entities.domain_entity import DomainEntity
from decision_engine.domain.errors.event_error import (
    EmptyEventPayloadError,
    EmptyEventTypeError,
    NegativeEventOccurredAtError,
    ZeroEventOccurredAtError,
)


class Event(DomainEntity):
    def __init__(
        self,
        *,
        event_type: str,
        payload: dict[str, Any],
        occurred_at: int,
        created_at: datetime | None = None,
        event_id: UUID | None = None,
    ) -> None:
        if not event_type.strip():
            raise EmptyEventTypeError

        if not payload:
            raise EmptyEventPayloadError

        if not occurred_at:
            raise ZeroEventOccurredAtError

        if occurred_at < 0:
            raise NegativeEventOccurredAtError(occurred_at=occurred_at)

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
