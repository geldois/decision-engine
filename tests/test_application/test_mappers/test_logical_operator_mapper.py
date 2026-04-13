import pytest

import app.application.mappers.logical_operator_mapper as LogicalOperatorMapper
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.operators.logical_operator import LogicalOperator


# ==========
# valid cases
# ==========
def test_parse_logical_operator_returns_valid_logical_operators() -> None:
    for member in LogicalOperator:
        assert (
            LogicalOperatorMapper.parse_logical_operator(value=member.value) is member
        )


# ==========
# invalid cases
# ==========
def test_parse_logical_operator_raises_when_value_is_invalid() -> None:
    with pytest.raises(ConditionException):
        LogicalOperatorMapper.parse_logical_operator(value="TEST")
