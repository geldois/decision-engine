from __future__ import annotations

from app.domain.exceptions.domain_exception import DomainException


class EventException(DomainException):
    @classmethod
    def event_payload_cannot_be_empty(cls) -> EventException:
        return cls("Event payload cannot be empty")

    @classmethod
    def event_type_cannot_be_empty(cls) -> EventException:
        return cls("Event type cannot be empty")

    @classmethod
    def event_timestamp_cannot_be_negative(cls, timestamp: int) -> EventException:
        return cls(f"Event timestamp cannot be negative (timestamp: {timestamp})")

    @classmethod
    def event_timestamp_cannot_be_zero(cls, timestamp: int) -> EventException:
        return cls(f"Event timestamp cannot be zero (timestamp: {timestamp})")
