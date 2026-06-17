from __future__ import annotations

from typing import override

from decision_engine.domain.errors.domain_error import DomainError


class ConditionError(DomainError, error_code=None): ...


class InvalidConditionError(ConditionError, error_code="CONDITION_INVALID"):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Condition is invalid."


class EmptyConditionOperatorError(
    ConditionError, error_code="CONDITION_OPERATOR_EMPTY"
):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Condition operator cannot be empty."


class InvalidConditionOperatorError(
    ConditionError, error_code="CONDITION_OPERATOR_INVALID"
):
    operator: str

    @override
    def __init__(self, *, operator: str) -> None:
        super().__init__(operator=operator)

    @override
    def _build_message(self) -> str:
        return f"Invalid condition operator: '{self.operator}'."


class InvalidConditionTypeError(ConditionError, error_code="CONDITION_TYPE_INVALID"):
    condition_type: str

    @override
    def __init__(self, *, condition_type: str) -> None:
        super().__init__(condition_type=condition_type)

    @override
    def _build_message(self) -> str:
        return f"Invalid condition type: '{self.condition_type}'."


class EmptyConditionValueError(ConditionError, error_code="CONDITION_VALUE_EMPTY"):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Condition value cannot be empty."


class MissingConditionFieldsError(
    ConditionError, error_code="CONDITION_MISSING_FIELDS"
):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "Condition fields are missing."
