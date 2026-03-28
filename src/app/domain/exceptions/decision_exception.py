from __future__ import annotations

from typing import Any

from app.domain.exceptions.domain_exception import DomainException


class DecisionException(DomainException):
    @classmethod
    def decision_explanation_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision explanation cannot be empty",
            exception_code="DECISION_EXPLANATION_EMPTY",
            details=details,
        )

    @classmethod
    def decision_not_found(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision not found",
            exception_code="DECISION_NOT_FOUND",
            details=details,
        )

    @classmethod
    def decision_with_rule_cannot_be_no_match(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision with rule cannot be no_match",
            exception_code="DECISION_OUTCOME_INVALID",
            details=details,
        )

    @classmethod
    def decision_without_rule_must_be_no_match(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision without rule must be no_match",
            exception_code="DECISION_OUTCOME_INVALID",
            details=details,
        )
