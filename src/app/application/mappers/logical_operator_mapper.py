from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.operators.logical_operator import LogicalOperator


def parse_logical_operator(
    value: str,
) -> LogicalOperator:
    if not value.strip():
        raise ConditionException.condition_operator_cannot_be_empty(
            details={"condition_operator": value}
        )

    try:
        return LogicalOperator(value)
    except ValueError as exception:
        raise ConditionException.condition_operator_is_invalid(
            details={"condition_operator": value}
        ) from exception
