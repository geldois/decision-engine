import pytest

import app.application.mappers.comparison_operator_mapper as ComparisonOperatorMapper
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


# ==========
# valid cases
# ==========
def test_parse_comparison_operator_returns_valid_comparison_operators() -> None:
    for member in ComparisonOperator:
        assert (
            ComparisonOperatorMapper.parse_comparison_operator(value=member.value)
            is member
        )


# ==========
# invalid cases
# ==========
def test_parse_comparison_operator_raises_when_value_is_invalid() -> None:
    with pytest.raises(ConditionException):
        ComparisonOperatorMapper.parse_comparison_operator(value="TEST")
