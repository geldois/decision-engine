from app.application.mappers.exposible_event_field_mapper import (
    map_exposible_event_field_to_domain,
    map_exposible_event_field_to_dto,
)
from app.application.types.exposible_event_field import (
    ExposibleEventField as DtoExposibleEventField,
)
from app.domain.entities.events.event import ExposibleEventField


# ==========
# valid
# ==========
def test_map_exposible_event_field_to_dto_returns_valid_dto_exposible_event_fields():
    for member in ExposibleEventField:
        assert (
            map_exposible_event_field_to_dto(member)
            is DtoExposibleEventField[member.name]
        )


def test_map_exposible_event_field_to_domain_returns_valid_domain_exposible_event_fields():
    for member in DtoExposibleEventField:
        assert map_exposible_event_field_to_domain(member) is ExposibleEventField(
            member.value
        )
