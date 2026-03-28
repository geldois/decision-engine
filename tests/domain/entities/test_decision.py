from uuid import uuid4

import pytest

from app.domain.entities.decision import Decision
from app.domain.exceptions.decision_exception import DecisionException
from app.domain.value_objects.decision_outcome import DecisionOutcome


# ==========
# invalid
# ==========
def test_decision_raises_decision_exception_when_explanation_is_empty() -> None:
    with pytest.raises(DecisionException):
        Decision(
            event_id=uuid4(),
            rule_id=uuid4(),
            outcome=DecisionOutcome.APPROVED,
            explanation=" ",
        )


def test_decision_raises_decision_exception_when_outcome_is_invalid() -> None:
    with pytest.raises(DecisionException):
        Decision(
            event_id=uuid4(),
            rule_id=uuid4(),
            outcome=DecisionOutcome.NO_MATCH,
            explanation="test",
        )

    with pytest.raises(DecisionException):
        Decision(
            event_id=uuid4(),
            rule_id=None,
            outcome=DecisionOutcome.APPROVED,
            explanation="test",
        )
