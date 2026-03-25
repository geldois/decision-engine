from app.application.types.exposible_event_field import (
    ExposibleEventField as DtoExposibleEventField,
)
from app.domain.entities.events.event import ExponibleEventField

_MAPPING = {
    ExponibleEventField.EVENT_ID: DtoExposibleEventField.EVENT_ID,
    ExponibleEventField.EVENT_TYPE: DtoExposibleEventField.EVENT_TYPE,
    ExponibleEventField.TIMESTAMP: DtoExposibleEventField.TIMESTAMP,
}


def map_exposible_event_field_to_dto(
    event_field: ExponibleEventField,
) -> DtoExposibleEventField:
    return _MAPPING[event_field]


def map_exposible_event_field_to_domain(
    event_field: DtoExposibleEventField | str,
) -> ExponibleEventField:
    if isinstance(event_field, DtoExposibleEventField):
        return ExponibleEventField(event_field.value)

    return ExponibleEventField(event_field)
