from app.application.types.exposible_event_field import (
    ExposibleEventField as DtoEventField,
)
from app.domain.entities.events.event import ExposibleEventField

_MAPPING = {
    ExposibleEventField.EVENT_ID: DtoEventField.EVENT_ID,
    ExposibleEventField.EVENT_TYPE: DtoEventField.EVENT_TYPE,
    ExposibleEventField.TIMESTAMP: DtoEventField.TIMESTAMP,
}


def map_exposible_event_field_to_dto(event_field: ExposibleEventField) -> DtoEventField:
    return _MAPPING[event_field]


def map_exposible_event_field_to_domain(
    event_field: DtoEventField | str,
) -> ExposibleEventField:
    if isinstance(event_field, DtoEventField):
        return ExposibleEventField(event_field.value)

    return ExposibleEventField(event_field)
