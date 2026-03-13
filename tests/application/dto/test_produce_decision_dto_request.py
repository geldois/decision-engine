from uuid import UUID, uuid4

from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest

# tests
def test_produce_decision_dto_request_exposes_only_boundary_fields():
    produce_decision_dto_request = ProduceDecisionDtoRequest(
        event_id = uuid4()
    )
    
    assert isinstance(produce_decision_dto_request.event_id, UUID)
    
    assert set(produce_decision_dto_request.__slots__) == {
        "event_id"
    }
    