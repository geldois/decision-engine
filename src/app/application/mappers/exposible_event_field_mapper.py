from app.application.types.exposible_event_field import (
    ExposibleEventField as DtoExposibleEventField,
)
from app.domain.entities.events.event import ExposibleEventField

_MAPPING = {
    ExposibleEventField.EVENT_ID: DtoExposibleEventField.EVENT_ID,
    ExposibleEventField.EVENT_TYPE: DtoExposibleEventField.EVENT_TYPE,
    ExposibleEventField.TIMESTAMP: DtoExposibleEventField.TIMESTAMP,
}


def map_exposible_event_field_to_dto(
    event_field: ExposibleEventField,
) -> DtoExposibleEventField:
    return _MAPPING[event_field]


def map_exposible_event_field_to_domain(
    event_field: DtoExposibleEventField | str,
) -> ExposibleEventField:
    if isinstance(event_field, DtoExposibleEventField):
        return ExposibleEventField(event_field.value)

    return ExposibleEventField(event_field)
