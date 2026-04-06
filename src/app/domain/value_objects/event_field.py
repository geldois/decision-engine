from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID

from app.domain.entities.event import Event


class EventField(Enum):
    expected_type: type[Any]

    EVENT_ID = ("id", UUID)
    EVENT_TYPE = ("event_type", str)
    TIMESTAMP = ("occurred_at", int)

    def __new__(cls, event_field: str, expected_type: type[Any]) -> EventField:
        obj = object.__new__(cls)
        obj._value_ = event_field
        obj.expected_type = expected_type

        return obj

    def get_field_value(self, event: Event):
        return getattr(event, self._value_)
