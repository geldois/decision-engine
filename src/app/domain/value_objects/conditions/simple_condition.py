from typing import Any

from app.domain.entities.event import Event
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.conditions.condition import Condition
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


class SimpleCondition(Condition):
    def __init__(
        self,
        operator: ComparisonOperator,
        field: EventField,
        value: Any,
    ) -> None:
        if operator in (
            ComparisonOperator.GREATER_THAN,
            ComparisonOperator.LESS_THAN,
        ) and not isinstance(value, int):
            raise ConditionException.condition_is_invalid(
                details={"field": field, "operator": operator, "value": value}
            )

        if not isinstance(value, field.expected_type):
            raise ConditionException.condition_is_invalid(
                details={"field": field, "operator": operator, "value": value}
            )

        self.operator = operator
        self.field = field
        self.value = value

    def evaluate(self, event: Event) -> bool:
        return self.operator.evaluate(
            left=self.field.get_field_value(event=event),
            right=self.value,
        )
