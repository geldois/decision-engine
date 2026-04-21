import pytest

from app.application.mappers.event_field_mapper import parse_event_field
from app.domain.exceptions.event_exception import EventException
from app.domain.value_objects.event_field import EventField

# VALID CASES


def test_parse_event_field_returns_valid_event_fields() -> None:
    for member in EventField:
        assert parse_event_field(value=member.value) is member


# INVALID CASES


def test_parse_event_field_raises_when_value_is_invalid() -> None:
    with pytest.raises(EventException):
        parse_event_field(value="TEST")
