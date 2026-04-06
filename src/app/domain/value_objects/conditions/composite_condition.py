from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.conditions.condition_contract import ConditionContract
from app.domain.value_objects.operators.logical_operator import LogicalOperator


class CompositeCondition(ConditionContract):
    def __init__(
        self, operator: LogicalOperator, conditions: list[ConditionContract]
    ) -> None:
        if len(conditions) < 2:
            raise ConditionException.condition_list_is_invalid(
                details={"conditions": conditions}
            )

        self.operator = operator
        self.conditions = conditions

    def compare(self) -> bool:
        conditions = (condition.compare() for condition in self.conditions)

        return self.operator.compare(conditions=conditions)
