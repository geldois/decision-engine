from __future__ import annotations

from typing import Any

from app.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    ConditionRegistry,
    ConditionVisitor,
    SimpleCondition,
)


class ConditionDeserializer:
    @staticmethod
    def deserialize(data: dict[str, Any]) -> Condition:
        return ConditionRegistry.get_class(data["type"]).from_dict(data=data)


class ConditionSerializer(ConditionVisitor[dict[str, Any]]):
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
    def serialize(cls, condition: Condition) -> dict[str, Any]:
        return condition.accept(visitor=cls)
