from app.application.types.event_field import EventField as DtoEventField
from app.domain.entities.events.event import EventField

_MAPPING = {
    EventField.EVENT_ID: DtoEventField.EVENT_ID,
    EventField.EVENT_TYPE: DtoEventField.EVENT_TYPE,
    EventField.TIMESTAMP: DtoEventField.TIMESTAMP,
}


def map_event_field_to_dto(event_field: EventField) -> DtoEventField:
    return _MAPPING[event_field]


def map_event_field_to_domain(event_field: DtoEventField | str) -> EventField:
    if isinstance(event_field, DtoEventField):
        return EventField(event_field.value)

    return EventField(event_field)
