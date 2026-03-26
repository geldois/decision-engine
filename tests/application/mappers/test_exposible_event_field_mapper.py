from app.application.mappers.exponible_event_field_mapper import (
    map_exponible_event_field_to_domain,
    map_exponible_event_field_to_dto,
)
from app.application.types.exponible_event_field import (
    ExponibleEventField as DtoExponibleEventField,
)
from app.domain.value_objects.exponible_event_field import ExponibleEventField


# ==========
# valid
# ==========
def test_map_exponible_event_field_to_dto_returns_valid_dto_exponible_event_fields():
    for member in ExponibleEventField:
        assert (
            map_exponible_event_field_to_dto(member)
            is DtoExponibleEventField[member.name]
        )


def test_map_exponible_event_field_to_domain_returns_valid_domain_exponible_event_fields():
    for member in DtoExponibleEventField:
        assert map_exponible_event_field_to_domain(member) is ExponibleEventField(
            member.value
        )
