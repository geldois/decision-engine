from uuid import uuid4

from app.domain.entities.event import Event
from app.domain.value_objects.event_field import EventField


class FakeType:
    pass


# ==========
# valid cases
# ==========
def test_event_field_returns_valid_bool_when_receives_invalid_value_type() -> None:
    fake_type_obj = FakeType()

    assert EventField.EVENT_ID.validate(value=uuid4())

    assert EventField.EVENT_TYPE.validate(value="TEST")

    assert EventField.OCCURRED_AT.validate(value=1700000000)

    assert EventField.PAYLOAD.validate(value={"test": True})

    assert not EventField.EVENT_ID.validate(value=fake_type_obj)

    assert not EventField.EVENT_TYPE.validate(value=fake_type_obj)

    assert not EventField.OCCURRED_AT.validate(value=fake_type_obj)

    assert not EventField.PAYLOAD.validate(value=fake_type_obj)


def test_event_field_returns_valid_field_values() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )

    for member in EventField:
        assert member.get_field_value(event=event) == getattr(event, member.value)
