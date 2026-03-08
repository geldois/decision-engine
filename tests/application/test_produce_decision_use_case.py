from app.application.dto.decision_status import DecisionStatus
from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.mappers.decision_outcome_to_status_mapper import map_outcome_to_status
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.events.event import EventField
from app.domain.rules.rule import Rule, RuleOperator
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository

# tests
def test_produce_decision_use_case_returns_reponse_with_status():
    produce_decision_use_case = ProduceDecisionUseCase(
        event_repository = InMemoryEventRepository(), 
        rule_repository = InMemoryRuleRepository(), 
        decision_engine = DecisionEngine()
    )
    produce_decision_dto_request = ProduceDecisionDtoRequest(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    
    produce_decision_dto_response = produce_decision_use_case.produce_decision(produce_decision_dto_request)
    
    assert produce_decision_dto_response.event_id
    
    assert DecisionStatus(produce_decision_dto_response.status)

def test_produce_decision_use_case_returns_response_with_the_same_rule_outcome_when_rule_applies():
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    rule_repository = InMemoryRuleRepository()
    rule_repository.save(rule)
    produce_decision_use_case = ProduceDecisionUseCase(
        event_repository = InMemoryEventRepository(), 
        rule_repository = rule_repository, 
        decision_engine = DecisionEngine()
    )
    produce_decision_dto_request = ProduceDecisionDtoRequest(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    
    produce_decision_dto_response = produce_decision_use_case.produce_decision(produce_decision_dto_request = produce_decision_dto_request)
    
    assert produce_decision_dto_response.event_id
    
    assert produce_decision_dto_response.status is map_outcome_to_status(DecisionOutcome.APPROVED)

def test_produce_decision_use_case_returns_response_with_no_match_outcome_when_no_rule_applies():
    rule = Rule(
        name = "NEVER_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.NOT_EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.REJECTED
    )
    rule_repository = InMemoryRuleRepository()
    rule_repository.save(rule)
    produce_decision_use_case = ProduceDecisionUseCase(
        event_repository = InMemoryEventRepository(), 
        rule_repository = rule_repository, 
        decision_engine = DecisionEngine()
    )
    produce_decision_dto_request = ProduceDecisionDtoRequest(
        event_type = "USER_CREATED",
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        },
        timestamp = 1700000000
    )
    
    produce_decision_dto_response = produce_decision_use_case.produce_decision(produce_decision_dto_request = produce_decision_dto_request)
    
    assert produce_decision_dto_response.event_id
    
    assert produce_decision_dto_response.status is DecisionStatus.NO_MATCH
