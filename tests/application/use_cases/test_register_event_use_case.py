from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.bootstrap.bootstrap import bootstrap


# ==========
# valid cases
# ==========
def test_register_event_use_case_returns_valid_dto_response() -> None:
    container = bootstrap(env="test")
    dto_register_event_request = DTORegisterEventRequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )

    dto_register_event_response = container.register_event_use_case.execute(
        dto_request=dto_register_event_request
    )

    assert (
        dto_register_event_response.event_type == dto_register_event_request.event_type
    )

    assert dto_register_event_response.payload == dto_register_event_request.payload

    assert (
        dto_register_event_response.occurred_at
        == dto_register_event_request.occurred_at
    )

    assert dto_register_event_response.event_id
