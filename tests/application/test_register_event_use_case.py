from app.domain.rules.rule import Rule
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository
from app.domain.services.decision_engine import DecisionEngine
from app.application.use_cases.register_event import RegisterEvent
from app.application.dto.decision_status import DecisionStatus
from app.application.dto.register_event_request import RegisterEventRequest
from app.application.dto.register_event_response import RegisterEventResponse

# === VALID CASE ===
def test_register_event_returns_reponse_with_status():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    event_repository = InMemoryEventRepository()
    rule_repository = InMemoryRuleRepository()
    decision_service = DecisionEngine()
    register_event = RegisterEvent(
        event_repository = event_repository, 
        rule_repository = rule_repository, 
        decision_service = decision_service
    )
    register_event_request = RegisterEventRequest(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    
    # WHEN
    register_event_response = register_event.register_event(register_event_request)
    
    # THEN
    assert register_event_response.event_id is not None
    
    assert register_event_response.status in (DecisionStatus.APPROVED, DecisionStatus.REJECTED)

# === RULE APPLIES ===
def test_register_event_returns_approved_response_when_rule_applies():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    name = "ALWAYS_APPLIES"
    condition = lambda event: True
    outcome = "approved"
    event_repository = InMemoryEventRepository()
    rule = Rule(
        name = name, 
        condition = condition, 
        outcome = outcome
    )
    rule_repository = InMemoryRuleRepository()
    rule_repository.save(rule)
    decision_service = DecisionEngine()
    register_event = RegisterEvent(
        event_repository = event_repository, 
        rule_repository = rule_repository, 
        decision_service = decision_service
    )
    register_event_request = RegisterEventRequest(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    
    # WHEN
    register_event_response = register_event.register_event(register_event_request)
    
    # THEN
    assert register_event_response.event_id is not None
    
    assert register_event_response.status == DecisionStatus.APPROVED

# === NO RULE APPLIES ===
def test_register_event_returns_rejected_response_when_no_rule_applies():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    name = "NEVER_APPLIES"
    condition = lambda event: False
    outcome = "unused"
    event_repository = InMemoryEventRepository()
    rule = Rule(
        name = name, 
        condition = condition, 
        outcome = outcome
    )
    rule_repository = InMemoryRuleRepository()
    rule_repository.save(rule)
    decision_service = DecisionEngine()
    register_event = RegisterEvent(
        event_repository = event_repository, 
        rule_repository = rule_repository, 
        decision_service = decision_service
    )
    register_event_request = RegisterEventRequest(
        event_type = event_type,
        payload = payload,
        timestamp = timestamp
    )
    
    # WHEN
    register_event_response = register_event.register_event(register_event_request)
    
    # THEN
    assert register_event_response.event_id is not None
    
    assert register_event_response.status == DecisionStatus.REJECTED
