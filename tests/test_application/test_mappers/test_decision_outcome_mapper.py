from __future__ import annotations

import pytest

from decision_engine.application.mappers.decision_outcome_mapper import (
    parse_decision_outcome,
)
from decision_engine.domain.errors.decision_error import DecisionError
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome

# VALID CASES


def test_parse_decision_outcome_always_returns_valid_outcomes() -> None:
    for member in DecisionOutcome:
        assert parse_decision_outcome(value=member.value) is member


# INVALID CASES


def test_parse_decision_outcome_raises_when_value_is_invalid() -> None:
    with pytest.raises(DecisionError):
        parse_decision_outcome(value="TEST")
