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
        if not field.validate(value=value):
            raise ConditionException.condition_is_invalid(
                details={"field": field, "operator": operator, "value": value}
            )

        self.operator = operator
        self.field = field
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimpleCondition):
            return False

        return (
            self.operator is other.operator
            and self.field is other.field
            and self.value == other.value
        )

    def evaluate(self, event: Event) -> bool:
        field_value = self.field.get_field_value(event=event)

        if not self.operator.validate(field=field_value, value=self.value):
            raise ConditionException.condition_is_invalid(
                details={
                    "field": self.field,
                    "operator": self.operator,
                    "value": self.value,
                }
            )

        return self.operator.evaluate(
            left=field_value,
            right=self.value,
        )
