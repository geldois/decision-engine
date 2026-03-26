from app.application.types.exponible_event_field import (
    ExponibleEventField as DtoExponibleEventField,
)
from app.domain.value_objects.exponible_event_field import ExponibleEventField


# ==========
# valid
# ==========
def test_dto_event_field_values_are_valid_event_fields():
    assert {member.name for member in DtoExponibleEventField} == {
        member.name for member in ExponibleEventField
    }
