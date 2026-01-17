from app.domain.events.event import Event
from app.domain.rules.rule import Rule
from app.services.decision_service import DecisionService

# === VALID CASE ===
def test_decision_service_returns_decision_when_rule_applies():
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
    decision_service = DecisionService()
    
    # WHEN
    decision = decision_service.decide(
        event = event, 
        rules = [rule]
    )
    
    # THEN
    assert decision.event == event
    
    assert decision.rule == rule
    
    assert decision.outcome == outcome
    
    assert decision.explanation is not None

# === NO RULE APPLIES ===
def test_decision_service_rejects_when_no_rule_applies():
    # GIVEN
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
    decision_service = DecisionService()
    
    # WHEN
    decision = decision_service.decide(
        event = event, 
        rules = []
    )
    
    # THEN
    assert decision.event == event
    
    assert decision.rule is None
    
    assert decision.outcome == "rejected"
    
    assert decision.explanation is not None
    