from app.domain.rules.rule import Rule
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.dto.decision_status import DecisionStatus
from app.application.dto.register_event_request import RegisterEventRequest
from app.application.dto.register_event_response import RegisterEventResponse
from app.application.mappers.decision_outcome_to_status_mapper import map_outcome_to_status

# tests
def test_register_event_returns_reponse_with_status():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    event_repository = InMemoryEventRepository()
    rule_repository = InMemoryRuleRepository()
    decision_engine = DecisionEngine()
    register_event = RegisterEventUseCase(
        event_repository = event_repository, 
        rule_repository = rule_repository, 
        decision_engine = decision_engine
    )
    register_event_request = RegisterEventRequest(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    
    register_event_response = register_event.register_event(register_event_request)
    
    assert register_event_response.event_id is not None
    
    assert DecisionStatus(register_event_response.status)

def test_register_event_returns_response_with_the_same_rule_outcome_when_rule_applies():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    name = "ALWAYS_APPLIES"
    condition = lambda event: True
    outcome = DecisionOutcome.APPROVED
    event_repository = InMemoryEventRepository()
    rule = Rule(
        name = name, 
        condition = condition, 
        outcome = outcome
    )
    rule_repository = InMemoryRuleRepository()
    rule_repository.save(rule)
    decision_engine = DecisionEngine()
    register_event = RegisterEventUseCase(
        event_repository = event_repository, 
        rule_repository = rule_repository, 
        decision_engine = decision_engine
    )
    register_event_request = RegisterEventRequest(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    
    register_event_response = register_event.register_event(register_event_request)
    
    assert register_event_response.event_id is not None
    
    assert register_event_response.status is map_outcome_to_status(outcome)

def test_register_event_returns_response_with_no_match_outcome_when_no_rule_applies():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    name = "NEVER_APPLIES"
    condition = lambda event: False
    outcome = DecisionOutcome.APPROVED
    event_repository = InMemoryEventRepository()
    rule = Rule(
        name = name, 
        condition = condition, 
        outcome = outcome
    )
    rule_repository = InMemoryRuleRepository()
    rule_repository.save(rule)
    decision_engine = DecisionEngine()
    register_event = RegisterEventUseCase(
        event_repository = event_repository, 
        rule_repository = rule_repository, 
        decision_engine = decision_engine
    )
    register_event_request = RegisterEventRequest(
        event_type = event_type,
        payload = payload,
        timestamp = timestamp
    )
    
    register_event_response = register_event.register_event(register_event_request)
    
    assert register_event_response.event_id is not None
    
    assert register_event_response.status is DecisionStatus.NO_MATCH
