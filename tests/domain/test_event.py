import pytest

from app.domain.events.event import Event

# tests
def test_event_can_be_created_with_valid_data():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    
    event = Event(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    
    assert event.event_type == event_type
    
    assert event.payload == payload
    
    assert event.timestamp == timestamp
    
    assert event.event_id is None

def test_event_raises_error_when_event_type_is_none():
    event_type = None
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp
        )

def test_event_raises_error_when_event_type_is_empty():
    event_type = " "
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp
        )

def test_event_raises_error_when_payload_is_none():
    event_type = "USER_CREATED"
    payload = None
    timestamp = 1700000000
    
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp
        )

def test_event_raises_error_when_timestamp_is_negative():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = -1700000000
    
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp
        )

def test_event_raises_error_when_event_id_is_negative():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    event_id = -1
    
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp,
            event_id = event_id
        )
        