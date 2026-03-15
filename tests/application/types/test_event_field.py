from app.application.types.event_field import EventField as DtoEventField
from app.domain.entities.events.event import EventField


def test_dto_event_field_values_are_valid_event_fields():
    assert {member.name for member in DtoEventField} == {
        member.name for member in EventField
    }
