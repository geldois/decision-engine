from typing import Any

from app.domain.entities.event import Event
from app.domain.value_objects.conditions.condition_contract import ConditionContract
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


class SimpleCondition(ConditionContract):
    def __init__(self, operator: ComparisonOperator, left: Any, right: Any) -> None:
        self.operator = operator
        self.left = left
        self.right = right

    def compare(self) -> bool:
        return self.operator.compare(left=self.left, right=self.right)

    def evaluate(self, event: Event) -> bool:
        return self.compare()
