from __future__ import annotations

from decision_engine.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    ConditionRegistry,
    ConditionVisitor,
    SimpleCondition,
)


class ConditionDeserializer:
    @staticmethod
    def deserialize(data: dict[str, object]) -> Condition:
        return ConditionRegistry.get_class(data["type"]).from_dict(data=data)


class ConditionSerializer(ConditionVisitor[dict[str, object]]):
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
    def serialize(cls, condition: Condition) -> dict[str, object]:
        return condition.accept(visitor=cls)
