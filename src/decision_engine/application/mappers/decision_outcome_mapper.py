from __future__ import annotations

from decision_engine.domain.errors.decision_error import InvalidDecisionOutcomeError
from decision_engine.domain.errors.rule_error import EmptyRuleOutcomeError
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome


def parse_decision_outcome(value: str) -> DecisionOutcome:
    if not value.strip():
        raise EmptyRuleOutcomeError

    try:
        return DecisionOutcome(value)
    except ValueError as exception:
        raise InvalidDecisionOutcomeError(outcome=value) from exception
