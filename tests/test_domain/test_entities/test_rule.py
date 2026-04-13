import pytest

from app.domain.entities.rule import Rule
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.condition import SimpleCondition
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


# ==========
# invalid cases
# ==========
def test_rule_raises_on_empty_name() -> None:
    with pytest.raises(RuleException):
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
    with pytest.raises(RuleException):
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
