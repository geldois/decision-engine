from __future__ import annotations

from typing import Any

from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.error_code import ErrorCode


class DecisionException(DomainException):
    @classmethod
    def decision_explanation_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision explanation cannot be empty",
            error_code=ErrorCode.DECISION_EXPLANATION_EMPTY,
            details=details,
        )

    @classmethod
    def decision_not_found(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision not found",
            error_code=ErrorCode.DECISION_NOT_FOUND,
            details=details,
        )

    @classmethod
    def decision_outcome_is_invalid(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision outcome is invalid",
            error_code=ErrorCode.DECISION_OUTCOME_INVALID,
            details=details,
        )

    @classmethod
    def decision_with_rule_cannot_be_no_match(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision with rule cannot be NO_MATCH",
            error_code=ErrorCode.DECISION_OUTCOME_INVALID,
            details=details,
        )

    @classmethod
    def decision_without_rule_must_be_no_match(
        cls, details: dict[str, Any] | None = None
    ) -> DecisionException:
        return cls(
            message="Decision without rule must be NO_MATCH",
            error_code=ErrorCode.DECISION_OUTCOME_INVALID,
            details=details,
        )
