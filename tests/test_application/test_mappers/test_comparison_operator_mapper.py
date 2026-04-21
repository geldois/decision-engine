import pytest

from app.application.mappers.comparison_operator_mapper import parse_comparison_operator
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator

# VALID CASES


def test_parse_comparison_operator_returns_valid_comparison_operators() -> None:
    for member in ComparisonOperator:
        assert parse_comparison_operator(value=member.value) is member


# INVALID CASES


def test_parse_comparison_operator_raises_when_value_is_invalid() -> None:
    with pytest.raises(ConditionException):
        parse_comparison_operator(value="TEST")
