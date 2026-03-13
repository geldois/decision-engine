from app.application.mappers.event_field_mapper import (
    map_event_field_to_domain,
    map_event_field_to_dto,
)
from app.application.types.event_field import EventField as DtoEventField
from app.domain.entities.events.event import EventField


def test_map_event_field_to_dto_always_returns_correct_dto_event_fields():
    for member in EventField:
        assert map_event_field_to_dto(member) is DtoEventField[member.name]


def test_map_event_field_to_domain_always_returns_correct_domain_event_fields():
    for member in DtoEventField:
        assert map_event_field_to_domain(member) is EventField(member.value)
