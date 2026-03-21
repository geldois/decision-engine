from app.application.types.exposible_event_field import (
    ExposibleEventField as DtoExposibleEventField,
)
from app.domain.entities.events.event import ExposibleEventField


# ==========
# valid
# ==========
def test_dto_event_field_values_are_valid_event_fields():
    assert {member.name for member in DtoExposibleEventField} == {
        member.name for member in ExposibleEventField
    }
