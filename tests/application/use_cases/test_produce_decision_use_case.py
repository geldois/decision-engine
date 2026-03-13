from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.mappers.decision_result_mapper import map_outcome_to_result
from app.application.types.decision_result import DecisionResult
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.events.event import Event, EventField
from app.domain.entities.rules.rule import Rule, RuleOperator
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.repositories.in_memory_decision_repository import InMemoryDecisionRepository
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository

# tests
def test_produce_decision_use_case_returns_valid_dto_response():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123, 
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event = event)
    produce_decision_use_case = ProduceDecisionUseCase(
        decision_repository = InMemoryDecisionRepository(), 
        event_repository = event_repository, 
        rule_repository = InMemoryRuleRepository(), 
        decision_engine = DecisionEngine()
    )
    produce_decision_dto_request = ProduceDecisionDtoRequest(event_id = saved_event._id)
    
    produce_decision_dto_response = produce_decision_use_case.produce_decision(produce_decision_dto_request = produce_decision_dto_request)
    
    assert produce_decision_dto_response.event_id == saved_event._id

    assert not produce_decision_dto_response.rule_id

    assert produce_decision_dto_response.status

    assert produce_decision_dto_response.explanation

    assert produce_decision_dto_response.decision_id
    
    assert DecisionResult(produce_decision_dto_response.status)

def test_produce_decision_use_case_returns_response_with_the_same_rule_outcome_when_rule_applies():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123, 
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event = event)
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    rule_repository = InMemoryRuleRepository()
    saved_rule = rule_repository.save(rule)
    produce_decision_use_case = ProduceDecisionUseCase(
        decision_repository = InMemoryDecisionRepository(), 
        event_repository = event_repository, 
        rule_repository = rule_repository, 
        decision_engine = DecisionEngine()
    )
    produce_decision_dto_request = ProduceDecisionDtoRequest(event_id = saved_event._id)
    
    produce_decision_dto_response = produce_decision_use_case.produce_decision(produce_decision_dto_request = produce_decision_dto_request)
    
    assert produce_decision_dto_response.event_id

    assert produce_decision_dto_response.rule_id == saved_rule._id
    
    assert produce_decision_dto_response.status is map_outcome_to_result(saved_rule.outcome)

def test_produce_decision_use_case_returns_response_with_no_match_outcome_when_no_rule_applies():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123, 
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event = event)
    rule = Rule(
        name = "NEVER_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.NOT_EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.REJECTED
    )
    rule_repository = InMemoryRuleRepository()
    saved_rule = rule_repository.save(rule)
    produce_decision_use_case = ProduceDecisionUseCase(
        decision_repository = InMemoryDecisionRepository(), 
        event_repository = event_repository, 
        rule_repository = rule_repository, 
        decision_engine = DecisionEngine()
    )
    produce_decision_dto_request = ProduceDecisionDtoRequest(event_id = saved_event._id)
    
    produce_decision_dto_response = produce_decision_use_case.produce_decision(produce_decision_dto_request = produce_decision_dto_request)
    
    assert produce_decision_dto_response.event_id
    
    assert produce_decision_dto_response.status is DecisionResult.NO_MATCH
