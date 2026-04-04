from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.operators.logical_operator import LogicalOperator


def map_logical_operator_by_name(
    logical_operator_name: str,
) -> LogicalOperator:
    return LogicalOperator[logical_operator_name]


def map_logical_operator_by_value(
    logical_operator_value: str,
) -> LogicalOperator:
    if not logical_operator_value.strip():
        raise ConditionException.condition_operator_cannot_be_empty(
            details={"condition_operator": logical_operator_value}
        )

    try:
        return LogicalOperator(logical_operator_value)
    except ValueError as exception:
        raise ConditionException.condition_operator_is_invalid(
            details={"condition_operator": logical_operator_value}
        ) from exception
