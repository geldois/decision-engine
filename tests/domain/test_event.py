from app.domain.events.event import Event

def test_event_can_be_created_with_valid_data():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    # WHEN
    event = Event(event_type, payload, timestamp)
    # THEN
    assert event.event_type == event_type
    assert event.payload == payload
    assert event.timestamp == timestamp
    assert event.event_id is None
