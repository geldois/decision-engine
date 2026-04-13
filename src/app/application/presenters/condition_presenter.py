from typing import Any

from app.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    SimpleCondition,
)
from app.domain.visitors.condition_visitor import ConditionVisitor


class ConditionPresenter(ConditionVisitor[dict[str, Any]]):
    def visit_composite(
        self,
        element: CompositeCondition,
    ) -> dict[str, Any]:
        return {
            "type": "composite",
            "operator": element.operator.value,
            "conditions": [
                condition.accept(visitor=self) for condition in element.conditions
            ],
        }

    def visit_simple(self, element: SimpleCondition) -> dict[str, Any]:
        return {
            "type": "simple",
            "field": element.field.value,
            "operator": element.operator.value,
            "value": element.value,
        }

    def present(self, element: Condition) -> dict[str, Any]:
        return element.accept(visitor=self)
