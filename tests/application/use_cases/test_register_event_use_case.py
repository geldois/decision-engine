from app.application.dto.register_event_dto_request import RegisterEventDtoRequest
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository

# tests
def test_register_event_use_case_returns_correct_dto_response():
    register_event_use_case = RegisterEventUseCase(event_repository = InMemoryEventRepository())
    register_event_dto_request = RegisterEventDtoRequest(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123, 
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )

    register_event_dto_response = register_event_use_case.register_event(register_event_dto_request = register_event_dto_request)

    assert register_event_dto_response.event_id

    assert register_event_dto_response.event_type == register_event_dto_request.event_type

    assert register_event_dto_response.payload == register_event_dto_request.payload

    assert register_event_dto_response.timestamp == register_event_dto_request.timestamp
    