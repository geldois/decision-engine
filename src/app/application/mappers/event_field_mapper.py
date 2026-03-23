from app.domain.exceptions.event_exception import EventException
from app.domain.value_objects.event_field import EventField


def map_event_field_by_name(
    event_field_name: str,
) -> EventField:
    return EventField[event_field_name]


def map_event_field_by_value(
    event_field_value: str,
) -> EventField:
    if not event_field_value.strip():
        raise EventException.event_field_cannot_be_empty(
            details={"event_field": event_field_value}
        )

    try:
        return EventField(event_field_value)
    except ValueError as exception:
        raise EventException.event_field_is_invalid(
            details={"event_field": event_field_value}
        ) from exception
