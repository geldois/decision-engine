from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


def map_comparison_operator_by_name(
    comparison_operator_name: str,
) -> ComparisonOperator:
    return ComparisonOperator[comparison_operator_name]


def map_comparison_operator_by_value(
    comparison_operator_value: str,
) -> ComparisonOperator:
    if not comparison_operator_value.strip():
        raise ConditionException.condition_operator_cannot_be_empty(
            details={"condition_operator": comparison_operator_value}
        )

    try:
        return ComparisonOperator(comparison_operator_value)
    except ValueError as exception:
        raise ConditionException.condition_operator_is_invalid(
            details={"condition_operator": comparison_operator_value}
        ) from exception
