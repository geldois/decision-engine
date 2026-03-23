import pytest

from app.application.mappers.decision_outcome_mapper import (
    map_outcome_by_name,
    map_outcome_by_value,
)
from app.domain.exceptions.decision_exception import DecisionException
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.decision_outcome import DecisionOutcome


# ==========
# valid cases
# ==========
def test_map_outcome_by_name_always_returns_valid_outcomes() -> None:
    for member in DecisionOutcome:
        assert map_outcome_by_name(outcome_name=member.name) is member


def test_map_outcome_by_value_always_returns_valid_outcomes() -> None:
    for member in DecisionOutcome:
        assert map_outcome_by_value(outcome_value=member.value) is member


# ==========
# invalid cases
# ==========
def test_map_outcome_by_value_raises_when_value_is_empty() -> None:
    with pytest.raises(RuleException):
        map_outcome_by_value(outcome_value=" ")


def test_map_outcome_by_value_raises_when_value_is_invalid() -> None:
    with pytest.raises(DecisionException):
        map_outcome_by_value(outcome_value="TEST")
