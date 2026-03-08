from dataclasses import fields
from dataclasses import FrozenInstanceError
from uuid import UUID, uuid4
import pytest

from app.application.dto.decision_status import DecisionStatus
from app.application.dto.produce_decision_dto_response import ProduceDecisionDtoResponse

#tests
def test_produce_decision_response_is_immutable():
    produce_decision_dto_response = ProduceDecisionDtoResponse(
        event_id = uuid4(), 
        status = DecisionStatus.APPROVED
    )
    
    assert isinstance(produce_decision_dto_response.event_id, UUID)
    
    assert isinstance(produce_decision_dto_response.status, DecisionStatus)
    
    assert {f.name for f in fields(ProduceDecisionDtoResponse)} == {
        "event_id",
        "status"
    }
    
    with pytest.raises(FrozenInstanceError):
        produce_decision_dto_response.event_id = uuid4()
    
    with pytest.raises(FrozenInstanceError):
        produce_decision_dto_response.status = DecisionStatus.REJECTED
