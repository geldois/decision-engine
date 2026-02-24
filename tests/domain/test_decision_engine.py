from app.domain.events.event import Event
from app.domain.rules.rule import Rule
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.domain.services.decision_engine import DecisionEngine

# tests
def test_decision_engine_returns_decision_when_rule_applies():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    name = "ALWAYS_APPLIES"
    condition = lambda event: True
    outcome = DecisionOutcome.APPROVED
    event = Event(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    rule = Rule(
        name = name, 
        condition = condition, 
        outcome = outcome
    )
    decision_engine = DecisionEngine()
    
    decision = decision_engine.decide(
        event = event, 
        rules = [rule]
    )
    
    assert decision.event == event
    
    assert decision.rule == rule
    
    assert decision.outcome is outcome
    
    assert decision.explanation is not None

def test_decision_engine_returns_decision_with_no_match_outcome_when_no_rule_applies():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    event = Event(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    decision_engine = DecisionEngine()
    
    decision = decision_engine.decide(
        event = event, 
        rules = []
    )
    
    assert decision.event == event
    
    assert decision.rule is None
    
    assert decision.outcome is DecisionOutcome.NO_MATCH
    
    assert decision.explanation is not None
    