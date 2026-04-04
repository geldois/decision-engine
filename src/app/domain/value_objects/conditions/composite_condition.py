from collections.abc import Sequence

from app.domain.entities.event import Event
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.conditions.condition import Condition
from app.domain.value_objects.operators.logical_operator import LogicalOperator


class CompositeCondition(Condition):
    def __init__(
        self, operator: LogicalOperator, conditions: Sequence[Condition]
    ) -> None:
        if len(conditions) < 2:
            raise ConditionException.condition_list_is_invalid(
                details={"conditions": conditions}
            )

        self.operator = operator
        self.conditions = conditions

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CompositeCondition):
            return False

        return self.operator is other.operator and self.conditions == self.conditions

    def evaluate(self, event: Event) -> bool:
        conditions = (condition.evaluate(event=event) for condition in self.conditions)

        return self.operator.evaluate(conditions=conditions)
