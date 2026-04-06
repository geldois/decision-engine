from __future__ import annotations

from typing import Any

from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.error_code import ErrorCode


class ConditionException(DomainException):
    @classmethod
    def condition_is_invalid(
        cls,
        details: dict[str, Any] | None = None,
    ) -> ConditionException:
        return cls(
            message="Condition is invalid",
            error_code=ErrorCode.CONDITION_INVALID,
            details=details,
        )

    @classmethod
    def condition_list_is_invalid(
        cls,
        details: dict[str, Any] | None = None,
    ) -> ConditionException:
        return cls(
            message="Condition list is invalid",
            error_code=ErrorCode.CONDITION_LIST_INVALID,
            details=details,
        )

    @classmethod
    def condition_operator_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> ConditionException:
        return cls(
            message="Condition operator cannot be empty",
            error_code=ErrorCode.CONDITION_OPERATOR_EMPTY,
            details=details,
        )

    @classmethod
    def condition_operator_is_invalid(
        cls, details: dict[str, Any] | None = None
    ) -> ConditionException:
        return cls(
            message="Condition operator is invalid",
            error_code=ErrorCode.CONDITION_OPERATOR_INVALID,
            details=details,
        )

    @classmethod
    def condition_value_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> ConditionException:
        return cls(
            message="Condition value cannot be empty",
            error_code=ErrorCode.CONDITION_VALUE_EMPTY,
            details=details,
        )
