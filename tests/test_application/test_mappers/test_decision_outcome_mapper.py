import pytest

import app.application.mappers.decision_outcome_mapper as DecisionOutcomeMapper
from app.domain.exceptions.decision_exception import DecisionException
from app.domain.value_objects.decision_outcome import DecisionOutcome


# ==========
# valid cases
# ==========
def test_parse_decision_outcome_always_returns_valid_outcomes() -> None:
    for member in DecisionOutcome:
        assert (
            DecisionOutcomeMapper.parse_decision_outcome(value=member.value) is member
        )


# ==========
# invalid cases
# ==========
def test_parse_decision_outcome_raises_when_value_is_invalid() -> None:
    with pytest.raises(DecisionException):
        DecisionOutcomeMapper.parse_decision_outcome(value="TEST")
