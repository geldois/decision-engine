from app.application.dto.register_event_dto_request import RegisterEventDtoRequest
from app.bootstrap.bootstrap import bootstrap


# ==========
# valid
# ==========
def test_register_event_use_case_returns_valid_dto_response():
    container = bootstrap(env="test")
    register_event_dto_request = RegisterEventDtoRequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )

    register_event_dto_response = container.register_event_use_case.execute(
        dto_request=register_event_dto_request
    )

    assert register_event_dto_response.event_id

    assert (
        register_event_dto_response.event_type == register_event_dto_request.event_type
    )

    assert register_event_dto_response.payload == register_event_dto_request.payload

    assert register_event_dto_response.timestamp == register_event_dto_request.timestamp
