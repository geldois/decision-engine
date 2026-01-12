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
    event = Event(event_type, payload, timestamp)
    rule = Rule(name, condition, outcome)
    service = DecisionService()
    # WHEN
    decision = service.decide(event, [rule])
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
    event = Event(event_type, payload, timestamp)
    service = DecisionService()
    # WHEN
    decision = service.decide(event, [])
    # THEN
    assert decision.event == event
    assert decision.rule is None
    assert decision.outcome == "rejected"
    assert decision.explanation is not None
    