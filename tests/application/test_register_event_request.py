from dataclasses import fields
from app.application.dto.register_event_request import RegisterEventRequest

# === VALID CASE ===
def test_register_event_request_exposes_only_boundary_fields():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    # WHEN
    register_event_request = RegisterEventRequest(event_type, payload, timestamp)
    # THEN
    assert isinstance(register_event_request.event_type, str)
    assert isinstance(register_event_request.payload, dict)
    assert isinstance(register_event_request.timestamp, int)
    assert set(register_event_request.__slots__) == {
        "event_type",
        "payload",
        "timestamp"
    }
    