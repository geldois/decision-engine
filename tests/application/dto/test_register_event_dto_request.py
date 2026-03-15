from app.application.dto.register_event_dto_request import RegisterEventDtoRequest


def test_register_event_dto_request_exposes_only_boundary_fields():
    register_event_dto_request = RegisterEventDtoRequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )

    assert isinstance(register_event_dto_request.event_type, str)

    assert isinstance(register_event_dto_request.payload, dict)

    assert isinstance(register_event_dto_request.timestamp, int)

    assert set(register_event_dto_request.__slots__) == {
        "event_type",
        "payload",
        "timestamp",
    }
