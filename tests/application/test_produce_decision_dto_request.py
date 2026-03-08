from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest

# tests
def test_produce_decision_dto_request_exposes_only_boundary_fields():
    produce_decision_dto_request = ProduceDecisionDtoRequest(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    
    assert isinstance(produce_decision_dto_request.event_type, str)
    
    assert isinstance(produce_decision_dto_request.payload, dict)
    
    assert isinstance(produce_decision_dto_request.timestamp, int)
    
    assert set(produce_decision_dto_request.__slots__) == {
        "event_type",
        "payload",
        "timestamp"
    }
    