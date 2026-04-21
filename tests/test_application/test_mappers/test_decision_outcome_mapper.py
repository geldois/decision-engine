import pytest

from app.application.mappers.decision_outcome_mapper import parse_decision_outcome
from app.domain.exceptions.decision_exception import DecisionException
from app.domain.value_objects.decision_outcome import DecisionOutcome

# VALID CASES


def test_parse_decision_outcome_always_returns_valid_outcomes() -> None:
    for member in DecisionOutcome:
        assert parse_decision_outcome(value=member.value) is member


# INVALID CASES


def test_parse_decision_outcome_raises_when_value_is_invalid() -> None:
    with pytest.raises(DecisionException):
        parse_decision_outcome(value="TEST")
