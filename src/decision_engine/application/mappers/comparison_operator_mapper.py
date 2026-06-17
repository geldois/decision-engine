from __future__ import annotations

from decision_engine.domain.errors.condition_error import (
    EmptyConditionOperatorError,
    InvalidConditionOperatorError,
)
from decision_engine.domain.value_objects.operators.comparison_operator import (
    ComparisonOperator,
)


def parse_comparison_operator(
    value: str,
) -> ComparisonOperator:
    if not value.strip():
        raise EmptyConditionOperatorError

    try:
        return ComparisonOperator(value)
    except ValueError as exception:
        raise InvalidConditionOperatorError(operator=value) from exception
