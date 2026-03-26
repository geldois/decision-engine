from app.application.types.exponible_event_field import (
    ExponibleEventField as DtoExponibleEventField,
)
from app.domain.value_objects.exponible_event_field import ExponibleEventField

_MAPPING = {
    ExponibleEventField.EVENT_ID: DtoExponibleEventField.EVENT_ID,
    ExponibleEventField.EVENT_TYPE: DtoExponibleEventField.EVENT_TYPE,
    ExponibleEventField.TIMESTAMP: DtoExponibleEventField.TIMESTAMP,
}


def map_exponible_event_field_to_dto(
    event_field: ExponibleEventField,
) -> DtoExponibleEventField:
    return _MAPPING[event_field]


def map_exponible_event_field_to_domain(
    event_field: DtoExponibleEventField | str,
) -> ExponibleEventField:
    if isinstance(event_field, DtoExponibleEventField):
        return ExponibleEventField(event_field.value)

    return ExponibleEventField(event_field)
