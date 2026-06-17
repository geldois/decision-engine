from __future__ import annotations

from typing import TYPE_CHECKING, override

from decision_engine.domain.errors.domain_error import DomainError

if TYPE_CHECKING:
    from uuid import UUID


class RuleError(DomainError, error_code=None): ...


class NotFoundRuleError(RuleError, error_code="RULE_NOT_FOUND"):
    rule_id: UUID

    @override
    def __init__(self, *, rule_id: UUID) -> None:
        super().__init__(rule_id=rule_id)

    @override
    def _build_message(self) -> str:
        return f"Rule '{self.rule_id}' was not found."


class EmptyRuleNameError(RuleError, error_code="RULE_NAME_EMPTY"):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Rule name cannot be empty."


class EmptyRuleOutcomeError(RuleError, error_code="RULE_OUTCOME_EMPTY"):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Rule outcome cannot be empty."


class InvalidRulePriorityError(RuleError, error_code="RULE_PRIORITY_INVALID"):
    priority: int

    @override
    def __init__(self, *, priority: int) -> None:
        super().__init__(priority=priority)

    @override
    def _build_message(self) -> str:
        return f"Invalid rule priority: {self.priority}."
