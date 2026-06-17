from __future__ import annotations

from decision_engine.domain.errors.condition_error import (
    EmptyConditionOperatorError,
    InvalidConditionOperatorError,
)
from decision_engine.domain.value_objects.operators.logical_operator import (
    LogicalOperator,
)


def parse_logical_operator(
    value: str,
) -> LogicalOperator:
    if not value.strip():
        raise EmptyConditionOperatorError

    try:
        return LogicalOperator(value)
    except ValueError as exception:
        raise InvalidConditionOperatorError(operator=value) from exception
