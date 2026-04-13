import json
from collections.abc import Callable
from typing import Any, Literal

from app.domain.value_objects.condition import (
    CompositeCondition,
    Condition,
    SimpleCondition,
)
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator
from app.domain.visitors.condition_visitor import ConditionVisitor


# ==========
# ConditionDeserializer
# ==========
def _deserialize_composite(data: dict[str, Any]) -> CompositeCondition:
    return CompositeCondition(
        operator=LogicalOperator(data["operator"]),
        conditions=[
            _deserialize_dict(data=condition) for condition in data["conditions"]
        ],
    )


def _deserialize_simple(data: dict[str, Any]) -> SimpleCondition:
    return SimpleCondition(
        operator=ComparisonOperator(data["operator"]),
        field=EventField(data["field"]),
        value=data["value"],
    )


_deserializers: dict[
    Literal["composite", "simple"], Callable[[dict[str, Any]], Condition]
] = {
    "composite": _deserialize_composite,
    "simple": _deserialize_simple,
}


def _deserialize_dict(data: dict[str, Any]) -> Condition:
    return _deserializers[data["type"]](data)


def deserialize(condition: str) -> Condition:
    data: dict[str, Any] = json.loads(condition)

    return _deserializers[data["type"]](data)


class ConditionSerializer(ConditionVisitor[dict[str, Any]]):
    def visit_composite(
        self,
        element: CompositeCondition,
    ) -> dict[str, Any]:
        return {
            "type": "composite",
            "operator": element.operator.value,
            "conditions": [c.accept(visitor=self) for c in element.conditions],
        }

    def visit_simple(self, element: SimpleCondition) -> dict[str, Any]:
        return {
            "type": "simple",
            "field": element.field.value,
            "operator": element.operator.value,
            "value": element.value,
        }

    def serialize(self, condition: Condition) -> str:
        return json.dumps(condition.accept(visitor=self))
