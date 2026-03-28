from __future__ import annotations

from typing import Any

from app.domain.exceptions.domain_exception import DomainException


class RuleException(DomainException):
    @classmethod
    def rule_condition_cannot_be_builded(
        cls,
        details: dict[str, Any] | None = None,
    ) -> RuleException:
        return cls(
            message="Rule condition cannot be builded",
            exception_code="RULE_CONDITION_INVALID",
            details=details,
        )

    @classmethod
    def rule_condition_value_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> RuleException:
        return cls(
            message="Rule condition value cannot be empty",
            exception_code="RULE_CONDITION_VALUE_EMPTY",
            details=details,
        )

    @classmethod
    def rule_name_cannot_be_empty(
        cls, details: dict[str, Any] | None = None
    ) -> RuleException:
        return cls(
            message="Rule name cannot be empty",
            exception_code="RULE_NAME_EMPTY",
            details=details,
        )

    @classmethod
    def rule_not_found(cls, details: dict[str, Any] | None = None) -> RuleException:
        return cls(
            message="Rule not found", exception_code="RULE_NOT_FOUND", details=details
        )
