import pytest

from app.domain.events.event import Event

# === VALID CASE ===
def test_event_can_be_created_with_valid_data():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    
    # WHEN
    event = Event(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    
    # THEN
    assert event.event_type == event_type
    
    assert event.payload == payload
    
    assert event.timestamp == timestamp
    
    assert event.event_id is None

# === INVALID event_type ===
def test_event_raises_error_when_event_type_is_none():
    # GIVEN
    event_type = None
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    
    # WHEN / THEN
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp
        )

def test_event_raises_error_when_event_type_is_empty():
    # GIVEN
    event_type = " "
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    
    # WHEN / THEN
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp
        )

# === INVALID payload ===
def test_event_raises_error_when_payload_is_none():
    # GIVEN
    event_type = "USER_CREATED"
    payload = None
    timestamp = 1700000000
    
    # WHEN / THEN
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp
        )

# === INVALID timestamp ===
def test_event_raises_error_when_timestamp_is_negative():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = -1700000000
    
    # WHEN / THEN
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp
        )

# === INVALID event_id ===
def test_event_raises_error_when_event_id_is_negative():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    event_id = -1
    
    # WHEN / THEN
    with pytest.raises(ValueError):
        Event(
            event_type = event_type, 
            payload = payload, 
            timestamp = timestamp,
            event_id = event_id
        )
        