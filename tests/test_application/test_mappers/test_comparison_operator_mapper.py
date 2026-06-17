import pytest

from decision_engine.application.mappers.comparison_operator_mapper import parse_comparison_operator
from decision_engine.domain.errors.condition_error import ConditionError
from decision_engine.domain.value_objects.operators.comparison_operator import ComparisonOperator

# VALID CASES


def test_parse_comparison_operator_returns_valid_comparison_operators() -> None:
    for member in ComparisonOperator:
        assert parse_comparison_operator(value=member.value) is member


# INVALID CASES


def test_parse_comparison_operator_raises_when_value_is_invalid() -> None:
    with pytest.raises(ConditionError):
        parse_comparison_operator(value="TEST")
