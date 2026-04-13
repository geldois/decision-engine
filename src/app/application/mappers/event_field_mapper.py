from app.domain.exceptions.event_exception import EventException
from app.domain.value_objects.event_field import EventField


def parse_event_field(
    value: str,
) -> EventField:
    if not value.strip():
        raise EventException.event_field_cannot_be_empty(details={"event_field": value})

    try:
        return EventField(value)
    except ValueError as exception:
        raise EventException.event_field_is_invalid(
            details={"event_field": value}
        ) from exception
