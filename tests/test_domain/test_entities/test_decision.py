from __future__ import annotations

from uuid import uuid4

import pytest

from decision_engine.domain.entities.decision import Decision
from decision_engine.domain.errors.decision_error import DecisionError
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome
from decision_engine.domain.value_objects.decision_trace import SimpleDecisionTrace
from decision_engine.domain.value_objects.event_field import EventField
from decision_engine.domain.value_objects.operators.comparison_operator import (
    ComparisonOperator,
)

# INVALID CASES


def test_decision_raises_when_outcome_is_invalid() -> None:
    with pytest.raises(DecisionError):
        Decision(
            event_id=uuid4(),
            rule_id=uuid4(),
            outcome=DecisionOutcome.NO_MATCH,
            traces=(
                SimpleDecisionTrace(
                    result=True,
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    expected_value="TEST",
                    actual_value="TEST",
                ),
            ),
        )

    with pytest.raises(DecisionError):
        Decision(
            event_id=uuid4(),
            rule_id=None,
            outcome=DecisionOutcome.APPROVED,
            traces=(
                SimpleDecisionTrace(
                    result=True,
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    expected_value="TEST",
                    actual_value="TEST",
                ),
            ),
        )
