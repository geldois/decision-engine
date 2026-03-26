from __future__ import annotations

from app.domain.exceptions.domain_exception import DomainException
from app.domain.value_objects.decision_outcome import DecisionOutcome


class DecisionException(DomainException):
    @classmethod
    def decision_explanation_cannot_be_empty(cls) -> DecisionException:
        return cls("Decision explanation cannot be empty")

    @classmethod
    def decision_with_rule_cannot_be_no_match(
        cls, outcome: DecisionOutcome
    ) -> DecisionException:
        return cls(f"Decision with rule cannot be {outcome}")

    @classmethod
    def decision_without_rule_must_be_no_match(
        cls, outcome: DecisionOutcome
    ) -> DecisionException:
        return cls(
            f"Decision without rule must be {DecisionOutcome.NO_MATCH} \
                (outcome: {outcome})"
        )
