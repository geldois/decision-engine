import pytest

from app.domain.entities.event import Event
from app.domain.exceptions.event_exception import EventException
from app.domain.value_objects.exponible_event_field import ExponibleEventField


# ==========
# valid
# ==========
def test_event_returns_valid_field_values():
    event_type = "USER_CREATED"
    payload = {"user_id": 123, "email": "user@email.com"}
    timestamp = 1700000000

    event = Event(event_type=event_type, payload=payload, timestamp=timestamp)

    for member in ExponibleEventField:
        assert event.get_field_value(exponible_event_field=member) == getattr(
            event, member.value
        )


# ==========
# invalid
# ==========
def test_event_raises_error_when_event_type_is_empty():
    event_type = " "
    payload = {"user_id": 123, "email": "user@email.com"}
    timestamp = 1700000000

    with pytest.raises(EventException):
        Event(event_type=event_type, payload=payload, timestamp=timestamp)


def test_event_raises_error_when_payload_is_empty():
    event_type = "USER_CREATED"
    payload = {}
    timestamp = 1700000000

    with pytest.raises(EventException):
        Event(event_type=event_type, payload=payload, timestamp=timestamp)


def test_event_raises_error_when_timestamp_is_negative_or_zero():
    event_type = "USER_CREATED"
    payload = {"user_id": 123, "email": "user@email.com"}
    timestamp = 0000000000

    with pytest.raises(EventException):
        Event(event_type=event_type, payload=payload, timestamp=timestamp)

    with pytest.raises(EventException):
        Event(event_type=event_type, payload=payload, timestamp=timestamp)
