import pytest

from app.application.mappers.comparison_operator_mapper import (
    map_comparison_operator_by_name,
    map_comparison_operator_by_value,
)
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.comparison_operator import ComparisonOperator


# ==========
# valid cases
# ==========
def test_map_comparison_operator_by_name_returns_valid_comparison_operators() -> None:
    for member in ComparisonOperator:
        assert (
            map_comparison_operator_by_name(comparison_operator_name=member.name)
            is member
        )


def test_map_comparison_operator_by_value_returns_valid_comparison_operators() -> None:
    for member in ComparisonOperator:
        assert (
            map_comparison_operator_by_value(comparison_operator_value=member.value)
            is member
        )


# ==========
# invalid cases
# ==========
def test_map_comparison_operator_by_value_raises_when_operator_value_is_empty() -> None:
    with pytest.raises(ConditionException):
        map_comparison_operator_by_value(comparison_operator_value=" ")


def test_map_comparison_operator_by_value_raises_when_operator_value_is_invalid() -> (
    None
):
    with pytest.raises(ConditionException):
        map_comparison_operator_by_value(comparison_operator_value="TEST")
