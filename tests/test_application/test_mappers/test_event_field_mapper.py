import pytest

import app.application.mappers.event_field_mapper as EventFieldMapper
from app.domain.exceptions.event_exception import EventException
from app.domain.value_objects.event_field import EventField


# ==========
# valid cases
# ==========
def test_parse_event_field_returns_valid_event_fields() -> None:
    for member in EventField:
        assert EventFieldMapper.parse_event_field(value=member.value) is member


# ==========
# invalid cases
# ==========
def test_parse_event_field_raises_when_value_is_invalid() -> None:
    with pytest.raises(EventException):
        EventFieldMapper.parse_event_field(value="TEST")
