from app.domain.events.event import Event, EventField
from app.domain.rules.rule import Rule, RuleOperator
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.services.decision_engine import DecisionEngine

# tests
def test_decision_engine_returns_decision_when_rule_applies():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123, 
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    rule = Rule(
        name = "ALWAYS_APPLIES", 
        condition_field = EventField.EVENT_TYPE, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = "USER_CREATED", 
        outcome = DecisionOutcome.APPROVED
    )
    decision_engine = DecisionEngine()
    
    decision = decision_engine.decide(
        event = event, 
        rules = [rule]
    )
    
    assert decision.event_id == event._id
    
    assert decision.rule_id == rule._id
    
    assert decision.outcome is DecisionOutcome.APPROVED
    
    assert decision.explanation

def test_decision_engine_returns_decision_with_no_match_outcome_when_no_rule_applies():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123, 
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    decision_engine = DecisionEngine()
    
    decision = decision_engine.decide(
        event = event, 
        rules = []
    )
    
    assert decision.event_id == event._id
    
    assert not decision.rule_id
    
    assert decision.outcome is DecisionOutcome.NO_MATCH
    
    assert decision.explanation
    