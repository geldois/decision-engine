import pytest

from app.domain.entities.event import Event
from app.domain.exceptions.event_exception import EventException
from app.domain.value_objects.event_field import EventField


# ==========
# valid cases
# ==========
def test_event_returns_valid_field_values() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )

    for member in EventField:
        assert event.get_field_value(event_field=member) == getattr(event, member.value)


# ==========
# invalid cases
# ==========
def test_event_raises_event_exception_when_payload_is_empty() -> None:
    with pytest.raises(EventException):
        Event(event_type="USER_CREATED", payload={}, timestamp=1700000000)


def test_event_raises_event_exception_when_timestamp_is_negative_or_zero():
    with pytest.raises(EventException):
        Event(
            event_type="USER_CREATED",
            payload={"user_id": 123, "email": "user@email.com"},
            timestamp=-1,
        )

    with pytest.raises(EventException):
        Event(
            event_type="USER_CREATED",
            payload={"user_id": 123, "email": "user@email.com"},
            timestamp=0000000000,
        )


def test_event_raises_event_exception_when_event_type_is_empty() -> None:
    with pytest.raises(EventException):
        Event(
            event_type=" ",
            payload={"user_id": 123, "email": "user@email.com"},
            timestamp=1700000000,
        )
