import pytest

from decision_engine.domain.entities.rule import Rule
from decision_engine.domain.errors.rule_error import RuleError
from decision_engine.domain.value_objects.condition import SimpleCondition
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome
from decision_engine.domain.value_objects.event_field import EventField
from decision_engine.domain.value_objects.operators.comparison_operator import ComparisonOperator

# INVALID CASES


def test_rule_raises_on_empty_name() -> None:
    with pytest.raises(RuleError):
        Rule(
            name=" ",
            condition=SimpleCondition(
                operator=ComparisonOperator.EQUALS,
                field=EventField.EVENT_TYPE,
                value="USER_CREATED",
            ),
            outcome=DecisionOutcome.APPROVED,
            priority=0,
        )


def test_rule_raises_on_negative_priority() -> None:
    with pytest.raises(RuleError):
        Rule(
            name="ALWAYS_APPLIES",
            condition=SimpleCondition(
                operator=ComparisonOperator.EQUALS,
                field=EventField.EVENT_TYPE,
                value="USER_CREATED",
            ),
            outcome=DecisionOutcome.APPROVED,
            priority=-1,
        )
