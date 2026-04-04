import pytest

from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.comparison_operator import ComparisonOperator
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField


# ==========
# valid cases
# ==========
def test_rule_returns_true_when_condition_is_true() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )

    assert rule.apply(event=event)


def test_rule_returns_false_when_condition_is_false() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.TIMESTAMP,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value=1800000000,
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )

    assert not rule.apply(event=event)


# ==========
# invalid cases
# ==========
def test_rule_raises_when_name_is_empty() -> None:
    with pytest.raises(RuleException):
        Rule(
            name=" ",
            condition_field=EventField.TIMESTAMP,
            condition_operator=ComparisonOperator.EQUALS,
            condition_value=1800000000,
            outcome=DecisionOutcome.APPROVED,
            priority=0,
        )


def test_rule_raises_when_priority_is_negative() -> None:
    with pytest.raises(RuleException):
        Rule(
            name="ALWAYS_APPLIES",
            condition_field=EventField.TIMESTAMP,
            condition_operator=ComparisonOperator.EQUALS,
            condition_value=1700000000,
            outcome=DecisionOutcome.APPROVED,
            priority=-1,
        )
