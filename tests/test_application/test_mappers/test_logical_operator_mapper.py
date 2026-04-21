import pytest

from app.application.mappers.logical_operator_mapper import parse_logical_operator
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.operators.logical_operator import LogicalOperator

# VALID CASES


def test_parse_logical_operator_returns_valid_logical_operators() -> None:
    for member in LogicalOperator:
        assert parse_logical_operator(value=member.value) is member


# INVALID CASES


def test_parse_logical_operator_raises_when_value_is_invalid() -> None:
    with pytest.raises(ConditionException):
        parse_logical_operator(value="TEST")
