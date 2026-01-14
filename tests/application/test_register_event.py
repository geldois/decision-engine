from app.domain.rules.rule import Rule
from app.application.register_event import RegisterEvent
from app.infrastructure.repositories.event_repository import EventRepository
from app.infrastructure.repositories.rule_repository import RuleRepository
from app.services.decision_service import DecisionService

# === VALID CASE ===
def test_register_event_creates_event_and_returns_decision():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    event_repository = EventRepository()
    rule_repository = RuleRepository()
    decision_service = DecisionService()
    register_event = RegisterEvent(event_repository, rule_repository, decision_service)
    # WHEN
    decision = register_event.register_event(event_type, payload, timestamp)
    # THEN
    assert decision is not None
    assert decision.outcome in ("approved", "rejected")

# === RULE APPLIES ===
def test_register_event_returns_approved_decision_when_rule_applies():
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
    event_repository = EventRepository()
    rule = Rule(name, condition, outcome)
    rule_repository = RuleRepository()
    rule_repository.save(rule)
    decision_service = DecisionService()
    register_event = RegisterEvent(event_repository, rule_repository, decision_service)
    # WHEN
    decision = register_event.register_event(event_type, payload, timestamp)
    # THEN
    assert decision.event.event_id is not None
    assert decision.rule is not None
    assert decision.outcome == "approved"

# === NO RULE APPLIES ===
def test_register_event_returns_rejected_decision_when_no_rule_applies():
    # GIVEN
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    name = "NEVER_APPLIES"
    condition = lambda event: False
    outcome = "irrelevant"
    event_repository = EventRepository()
    rule = Rule(name, condition, outcome)
    rule_repository = RuleRepository()
    rule_repository.save(rule)
    decision_service = DecisionService()
    register_event = RegisterEvent(event_repository, rule_repository, decision_service)
    # WHEN
    decision = register_event.register_event(event_type, payload, timestamp)
    # THEN
    assert decision.event.event_id is not None
    assert decision.rule is None
    assert decision.outcome == "rejected"
