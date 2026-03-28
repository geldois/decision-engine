from __future__ import annotations

from typing import Any

from app.domain.exceptions.domain_exception import DomainException


class EventException(DomainException):
    @classmethod
    def event_not_found(cls, details: dict[str, Any] | None = None) -> EventException:
        return cls(
            message="Event not found", exception_code="EVENT_NOT_FOUND", details=details
        )

    @classmethod
    def event_payload_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event payload cannot be empty",
            exception_code="EVENT_PAYLOAD_EMPTY",
            details=details,
        )

    @classmethod
    def event_timestamp_cannot_be_negative(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event timestamp cannot be negative",
            exception_code="EVENT_TIMESTAMP_INVALID",
            details=details,
        )

    @classmethod
    def event_timestamp_cannot_be_zero(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event timestamp cannot be zero",
            exception_code="EVENT_TIMESTAMP_INVALID",
            details=details,
        )

    @classmethod
    def event_type_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event type cannot be empty",
            exception_code="EVENT_TYPE_EMPTY",
            details=details,
        )
