import pytest

from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.exponible_event_field import ExponibleEventField
from app.domain.value_objects.rule_operator import RuleOperator


# ==========
# valid
# ==========
def test_rule_returns_true_when_condition_is_true() -> None:
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

    assert rule.applies_to(event=event)


# ==========
# invalid
# ==========
def test_rule_raises_error_when_name_is_empty() -> None:
    with pytest.raises(RuleException):
        Rule(
            name=" ",
            condition_field=ExponibleEventField.TIMESTAMP,
            condition_operator=RuleOperator.EQUALS,
            condition_value=1800000000,
            outcome=DecisionOutcome.APPROVED,
        )


def test_rule_raises_error_when_condition_value_is_zero_or_empty() -> None:
    with pytest.raises(RuleException):
        Rule(
            name="ALWAYS_APPLIES",
            condition_field=ExponibleEventField.TIMESTAMP,
            condition_operator=RuleOperator.EQUALS,
            condition_value=0000000000,
            outcome=DecisionOutcome.APPROVED,
        )

    with pytest.raises(RuleException):
        Rule(
            name="ALWAYS_APPLIES",
            condition_field=ExponibleEventField.TIMESTAMP,
            condition_operator=RuleOperator.EQUALS,
            condition_value=" ",
            outcome=DecisionOutcome.APPROVED,
        )


def test_rule_returns_false_when_condition_is_false() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=ExponibleEventField.TIMESTAMP,
        condition_operator=RuleOperator.EQUALS,
        condition_value=1800000000,
        outcome=DecisionOutcome.APPROVED,
    )

    assert not rule.applies_to(event=event)
