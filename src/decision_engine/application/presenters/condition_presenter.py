from __future__ import annotations

from decision_engine.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    ConditionVisitor,
    SimpleCondition,
)


class ConditionPresenter(ConditionVisitor[dict[str, object]]):
    @classmethod
    def visit_composite(
        cls,
        element: CompositeCondition,
    ) -> dict[str, object]:
        return {
            "type": "composite",
            "operator": element.operator.value,
            "conditions": [
                condition.accept(visitor=cls) for condition in element.conditions
            ],
        }

    @classmethod
    def visit_simple(cls, element: SimpleCondition) -> dict[str, object]:
        return {
            "type": "simple",
            "field": element.field.value,
            "operator": element.operator.value,
            "value": element.value,
        }

    @classmethod
    def present(cls, element: Condition) -> dict[str, object]:
        return element.accept(visitor=cls)
