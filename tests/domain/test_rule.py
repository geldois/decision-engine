from app.domain.events.event import Event, EventField
from app.domain.rules.rule import Rule, RuleOperator
from app.domain.decisions.decision_outcome import DecisionOutcome

# tests
def test_rule_returns_true_when_condition_is_true():
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

    assert rule.applies_to(event)
    
def test_rule_returns_false_when_condition_is_false():
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
        condition_field = EventField.TIMESTAMP, 
        condition_operator = RuleOperator.EQUALS, 
        condition_value = 1800000000, 
        outcome = DecisionOutcome.APPROVED
    )

    assert not rule.applies_to(event)
