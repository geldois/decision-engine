from app.domain.entities.events.event import Event
from app.domain.entities.rules.rule import Rule
from app.domain.services.decision_engine import DecisionEngine
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.exponible_event_field import ExponibleEventField
from app.domain.value_objects.rule_operator import RuleOperator


# ==========
# valid
# ==========
def test_decision_engine_returns_valid_decision_when_rule_applies():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=ExponibleEventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
    )
    decision_engine = DecisionEngine()

    decision = decision_engine.decide(event=event, rules=[rule])

    assert decision.event_id == event.id

    assert decision.rule_id == rule.id

    assert decision.outcome is rule.outcome

    assert decision.explanation


def test_decision_engine_returns_valid_decision_when_no_rule_applies():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    decision_engine = DecisionEngine()

    decision = decision_engine.decide(event=event, rules=[])

    assert decision.event_id == event.id

    assert not decision.rule_id

    assert decision.outcome is DecisionOutcome.NO_MATCH

    assert decision.explanation
