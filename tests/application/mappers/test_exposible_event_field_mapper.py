import pytest

from app.application.mappers.event_field_mapper import (
    map_event_field_by_name,
    map_event_field_by_value,
)
from app.domain.exceptions.event_exception import EventException
from app.domain.value_objects.event_field import EventField


# ==========
# valid cases
# ==========
def test_map_event_field_by_name_returns_valid_event_fields() -> None:
    for member in EventField:
        assert map_event_field_by_name(event_field_name=member.name) is member


def test_map_event_field_by_value_returns_valid_event_fields() -> None:
    for member in EventField:
        assert map_event_field_by_value(event_field_value=member.value) is member


# ==========
# invalid cases
# ==========
def test_map_event_field_by_value_raises_when_field_value_is_empty() -> None:
    with pytest.raises(EventException):
        map_event_field_by_value(event_field_value=" ")


def test_map_event_field_by_value_raises_when_field_value_is_invalid() -> None:
    with pytest.raises(EventException):
        map_event_field_by_value(event_field_value="TEST")
