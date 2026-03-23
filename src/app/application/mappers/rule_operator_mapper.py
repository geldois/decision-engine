from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.rule_operator import RuleOperator


def map_rule_operator_by_name(rule_operator_name: str) -> RuleOperator:
    return RuleOperator[rule_operator_name]


def map_rule_operator_by_value(rule_operator_value: str) -> RuleOperator:
    if not rule_operator_value.strip():
        raise RuleException.rule_condition_operator_cannot_be_empty(
            details={"condition_operator": rule_operator_value}
        )

    try:
        return RuleOperator(rule_operator_value)
    except ValueError as exception:
        raise RuleException.rule_condition_operator_is_invalid(
            details={"condition_operator": rule_operator_value}
        ) from exception
