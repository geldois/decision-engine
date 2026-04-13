import pytest

from app.domain.entities.event import Event
from app.domain.exceptions.event_exception import EventException


# ==========
# invalid cases
# ==========
def test_event_raises_on_empty_payload() -> None:
    with pytest.raises(EventException):
        Event(event_type="USER_CREATED", payload={}, occurred_at=1700000000)


def test_event_raises_on_negative_or_zero_occurred_at():
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


def test_event_raises_on_empty_event_type() -> None:
    with pytest.raises(EventException):
        Event(
            event_type=" ",
            payload={"user_id": 123, "email": "user@email.com"},
            occurred_at=1700000000,
        )
