from __future__ import annotations

from typing import Any

from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.error_code import ErrorCode


class EventException(DomainException):
    @classmethod
    def event_field_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event field cannot be empty",
            error_code=ErrorCode.EVENT_FIELD_EMPTY,
            details=details,
        )

    @classmethod
    def event_field_is_invalid(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event field is invalid",
            error_code=ErrorCode.EVENT_FIELD_INVALID,
            details=details,
        )

    @classmethod
    def event_not_found(cls, details: dict[str, Any] | None = None) -> EventException:
        return cls(
            message="Event not found",
            error_code=ErrorCode.EVENT_NOT_FOUND,
            details=details,
        )

    @classmethod
    def event_payload_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event payload cannot be empty",
            error_code=ErrorCode.EVENT_PAYLOAD_EMPTY,
            details=details,
        )

    @classmethod
    def event_occurred_at_cannot_be_negative(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event occurred_at cannot be negative",
            error_code=ErrorCode.EVENT_OCCURRED_AT_INVALID,
            details=details,
        )

    @classmethod
    def event_occurred_at_cannot_be_zero(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event occurred_at cannot be zero",
            error_code=ErrorCode.EVENT_OCCURRED_AT_INVALID,
            details=details,
        )

    @classmethod
    def event_type_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> EventException:
        return cls(
            message="Event type cannot be empty",
            error_code=ErrorCode.EVENT_TYPE_EMPTY,
            details=details,
        )
