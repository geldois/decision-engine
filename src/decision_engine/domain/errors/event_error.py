from __future__ import annotations

from typing import TYPE_CHECKING, override

from decision_engine.domain.errors.domain_error import DomainError

if TYPE_CHECKING:
    from uuid import UUID


class EventError(DomainError, error_code=None): ...


class NotFoundEventError(EventError, error_code="EVENT_NOT_FOUND"):
    event_id: UUID

    @override
    def __init__(self, *, event_id: UUID) -> None:
        super().__init__(event_id=event_id)

    @override
    def _build_message(self) -> str:
        return f"Event '{self.event_id}' was not found."


class EmptyEventTypeError(EventError, error_code="EVENT_TYPE_EMPTY"):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Event type cannot be empty."


class EmptyEventPayloadError(EventError, error_code="EVENT_PAYLOAD_EMPTY"):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Event payload cannot be empty."


class ZeroEventOccurredAtError(EventError, error_code="EVENT_OCCURRED_AT_INVALID"):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Event occurred_at cannot be zero."


class NegativeEventOccurredAtError(
    EventError, error_code="EVENT_OCCURRED_AT_INVALID"
):
    occurred_at: int

    @override
    def __init__(self, *, occurred_at: int) -> None:
        super().__init__(occurred_at=occurred_at)

    @override
    def _build_message(self) -> str:
        return f"Event occurred_at cannot be negative: {self.occurred_at}."


class EmptyEventFieldError(EventError, error_code="EVENT_FIELD_EMPTY"):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Event field cannot be empty."


class InvalidEventFieldError(EventError, error_code="EVENT_FIELD_INVALID"):
    field: str

    @override
    def __init__(self, *, field: str) -> None:
        super().__init__(field=field)

    @override
    def _build_message(self) -> str:
        return f"Invalid event field: '{self.field}'."
