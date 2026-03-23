import pytest

from app.application.mappers.rule_operator_mapper import (
    map_rule_operator_by_name,
    map_rule_operator_by_value,
)
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.rule_operator import RuleOperator


# ==========
# valid cases
# ==========
def test_map_rule_operator_by_name_returns_valid_rule_operators() -> None:
    for member in RuleOperator:
        assert map_rule_operator_by_name(rule_operator_name=member.name) is member


def test_map_rule_operator_by_value_returns_valid_rule_operators() -> None:
    for member in RuleOperator:
        assert map_rule_operator_by_value(rule_operator_value=member.value) is member


# ==========
# invalid cases
# ==========
def test_map_rule_operator_by_value_raises_when_operator_value_is_empty() -> None:
    with pytest.raises(RuleException):
        map_rule_operator_by_value(rule_operator_value=" ")


def test_map_rule_operator_by_value_raises_when_operator_value_is_invalid() -> None:
    with pytest.raises(RuleException):
        map_rule_operator_by_value(rule_operator_value="TEST")
