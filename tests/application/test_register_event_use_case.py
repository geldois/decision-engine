from app.application.dto.decision_status import DecisionStatus
from app.application.dto.register_event_request import RegisterEventRequest
from app.application.mappers.decision_outcome_to_status_mapper import map_outcome_to_status
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.events.event import EventField
from app.domain.rules.rule import Rule, RuleOperator
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository

# tests
def test_register_event_use_case_returns_reponse_with_status():
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

def test_register_event_use_case_returns_response_with_the_same_rule_outcome_when_rule_applies():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    name = "ALWAYS_APPLIES"
    condition_field = EventField.EVENT_TYPE
    condition_operator = RuleOperator.EQUALS
    condition_value = "USER_CREATED"
    outcome = DecisionOutcome.APPROVED
    event_repository = InMemoryEventRepository()
    rule = Rule(
        name = name, 
        condition_field = condition_field, 
        condition_operator = condition_operator, 
        condition_value = condition_value, 
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

def test_register_event_use_case_returns_response_with_no_match_outcome_when_no_rule_applies():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    name = "NEVER_APPLIES"
    condition_field = EventField.EVENT_TYPE
    condition_operator = RuleOperator.NOT_EQUALS
    condition_value = "USER_CREATED"
    outcome = DecisionOutcome.REJECTED
    event_repository = InMemoryEventRepository()
    rule = Rule(
        name = name, 
        condition_field = condition_field, 
        condition_operator = condition_operator, 
        condition_value = condition_value, 
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
