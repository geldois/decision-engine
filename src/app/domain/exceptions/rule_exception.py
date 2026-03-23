from __future__ import annotations

from typing import Any

from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.error_code import ErrorCode


class RuleException(DomainException):
    @classmethod
    def rule_condition_cannot_be_built(
        cls,
        details: dict[str, Any] | None = None,
    ) -> RuleException:
        return cls(
            message="Rule condition cannot be built",
            error_code=ErrorCode.RULE_CONDITION_INVALID,
            details=details,
        )

    @classmethod
    def rule_condition_operator_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> RuleException:
        return cls(
            message="Rule condition operator cannot be empty",
            error_code=ErrorCode.RULE_CONDITION_OPERATOR_EMPTY,
            details=details,
        )

    @classmethod
    def rule_condition_operator_is_invalid(
        cls, details: dict[str, Any] | None = None
    ) -> RuleException:
        return cls(
            message="Rule condition operator is invalid",
            error_code=ErrorCode.RULE_CONDITION_OPERATOR_INVALID,
            details=details,
        )

    @classmethod
    def rule_condition_value_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> RuleException:
        return cls(
            message="Rule condition value cannot be empty",
            error_code=ErrorCode.RULE_CONDITION_VALUE_EMPTY,
            details=details,
        )

    @classmethod
    def rule_name_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> RuleException:
        return cls(
            message="Rule name cannot be empty",
            error_code=ErrorCode.RULE_NAME_EMPTY,
            details=details,
        )

    @classmethod
    def rule_outcome_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> RuleException:
        return cls(
            message="Rule outcome cannot be empty",
            error_code=ErrorCode.RULE_OUTCOME_EMPTY,
            details=details,
        )

    @classmethod
    def rule_not_found(cls, details: dict[str, Any] | None = None) -> RuleException:
        return cls(
            message="Rule not found",
            error_code=ErrorCode.RULE_NOT_FOUND,
            details=details,
        )
