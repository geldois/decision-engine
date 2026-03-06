from enum import Enum

from app.domain.domain_entity import DomainEntity

class EventField(Enum):
    # enum members
    EVENT_ID = "event_id"
    EVENT_TYPE = "event_type"
    TIMESTAMP = "timestamp"

class Event(DomainEntity):
    __slots__ = (
        "event_id", 
        "event_type", 
        "payload", 
        "timestamp"
    )

    # initializer
    def __init__(
        self, 
        event_type: str, 
        payload: dict, 
        timestamp: int, 
        event_id: int | None = None
    ):
        # invariants
        if event_type is None or not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("Event type is required.")
        
        if payload is None:
            raise ValueError("Event payload is required.")
        
        if timestamp is None or not isinstance(timestamp, int) or timestamp < 0:
            raise ValueError("Event timestamp is required.")
        
        if event_id is not None and (not isinstance(event_id, int) or event_id < 0):
            raise ValueError("Event id is invalid.")
        
        # instance attributes
        self.event_type = event_type.strip()
        self.payload = payload
        self.timestamp = timestamp
        self.event_id = event_id

    # methods
    def get_field_value(
        self, 
        event_field: EventField
    ):
        return self.__getattribute__(event_field.value)
    