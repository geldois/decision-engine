from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


def parse_comparison_operator(
    value: str,
) -> ComparisonOperator:
    if not value.strip():
        raise ConditionException.condition_operator_cannot_be_empty(
            details={"condition_operator": value}
        )

    try:
        return ComparisonOperator(value)
    except ValueError as exception:
        raise ConditionException.condition_operator_is_invalid(
            details={"condition_operator": value}
        ) from exception
