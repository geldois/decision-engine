from typing import Any

from app.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    ConditionVisitor,
    SimpleCondition,
)


class ConditionPresenter(ConditionVisitor[dict[str, Any]]):
    @classmethod
    def visit_composite(
        cls,
        element: CompositeCondition,
    ) -> dict[str, Any]:
        return {
            "type": "composite",
            "operator": element.operator.value,
            "conditions": [
                condition.accept(visitor=cls) for condition in element.conditions
            ],
        }

    @classmethod
    def visit_simple(cls, element: SimpleCondition) -> dict[str, Any]:
        return {
            "type": "simple",
            "field": element.field.value,
            "operator": element.operator.value,
            "value": element.value,
        }

    @classmethod
    def present(cls, element: Condition) -> dict[str, Any]:
        return element.accept(visitor=cls)
