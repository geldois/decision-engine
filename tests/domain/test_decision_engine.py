from datetime import UTC, datetime

from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.services.decision_engine import DecisionEngine
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.rule_operator import RuleOperator


# ==========
# valid cases
# ==========
def test_decision_engine_returns_sorted_list_of_rules_by_priority_and_tie_breaking_criteria() -> (
    None
):
    rule_1 = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    rule_2 = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
        created_at=datetime(2026, 1, 2, tzinfo=UTC),
    )
    rule_3 = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=1,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    decision_engine = DecisionEngine()

    sorted_rules = decision_engine.sort_by_priority(rules=[rule_1, rule_2, rule_3])

    assert (
        sorted_rules[0] == rule_3
        and sorted_rules[1] == rule_2
        and sorted_rules[2] == rule_1
    )


def test_decision_engine_returns_valid_decision_when_rule_applies():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=RuleOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
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
        occurred_at=1700000000,
    )
    decision_engine = DecisionEngine()

    decision = decision_engine.decide(event=event, rules=[])

    assert decision.event_id == event.id

    assert not decision.rule_id

    assert decision.outcome is DecisionOutcome.NO_MATCH

    assert decision.explanation
