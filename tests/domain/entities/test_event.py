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
        occurred_at=1700000000,
    )

    for member in EventField:
        assert event.get_field_value(event_field=member) == getattr(event, member.value)


# ==========
# invalid cases
# ==========
def test_event_raises_when_payload_is_empty() -> None:
    with pytest.raises(EventException):
        Event(event_type="USER_CREATED", payload={}, occurred_at=1700000000)


def test_event_raises_when_occurred_at_is_negative_or_zero():
    with pytest.raises(EventException):
        Event(
            event_type="USER_CREATED",
            payload={"user_id": 123, "email": "user@email.com"},
            occurred_at=-1,
        )

    with pytest.raises(EventException):
        Event(
            event_type="USER_CREATED",
            payload={"user_id": 123, "email": "user@email.com"},
            occurred_at=0000000000,
        )


def test_event_raises_when_event_type_is_empty() -> None:
    with pytest.raises(EventException):
        Event(
            event_type=" ",
            payload={"user_id": 123, "email": "user@email.com"},
            occurred_at=1700000000,
        )
