import pytest
from dataclasses import FrozenInstanceError
from dataclasses import fields

from app.application.dto.decision_status import DecisionStatus
from app.application.dto.register_event_response import RegisterEventResponse

#tests
def test_register_event_response_is_immutable():
    event_id = 1
    status = DecisionStatus.APPROVED
    
    register_event_response = RegisterEventResponse(
        event_id = event_id, 
        status = status
    )
    
    assert isinstance(register_event_response.event_id, int)
    
    assert isinstance(register_event_response.status, DecisionStatus)
    
    assert {f.name for f in fields(RegisterEventResponse)} == {
        "event_id",
        "status"
    }
    
    with pytest.raises(FrozenInstanceError):
        register_event_response.event_id = 2
    
    with pytest.raises(FrozenInstanceError):
        register_event_response.status = DecisionStatus.REJECTED
