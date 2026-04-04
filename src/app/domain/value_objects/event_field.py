from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import UUID

from app.domain.entities.event import Event


class EventField(Enum):
    expected_types: tuple[type[Any], ...]

    EVENT_ID = "id", (UUID,)
    EVENT_TYPE = "event_type", (str,)
    OCCURRED_AT = "occurred_at", (int,)
    PAYLOAD = "payload", (dict,)

    def __new__(
        cls, event_field: str, expected_types: tuple[type[Any], ...]
    ) -> EventField:
        obj = object.__new__(cls)
        obj._value_ = event_field
        obj.expected_types = expected_types

        return obj

    def _is_valid_type(self, obj: Any) -> bool:
        return isinstance(obj, self.expected_types)

    def validate(self, value: Any) -> bool:
        return self._is_valid_type(obj=value)

    def get_field_value(self, event: Event):
        return getattr(event, self._value_)
