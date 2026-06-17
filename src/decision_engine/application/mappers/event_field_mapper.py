from __future__ import annotations

from decision_engine.domain.errors.event_error import (
    EmptyEventFieldError,
    InvalidEventFieldError,
)
from decision_engine.domain.value_objects.event_field import EventField


def parse_event_field(
    value: str,
) -> EventField:
    if not value.strip():
        raise EmptyEventFieldError

    try:
        return EventField(value)
    except ValueError as exception:
        raise InvalidEventFieldError(field=value) from exception
