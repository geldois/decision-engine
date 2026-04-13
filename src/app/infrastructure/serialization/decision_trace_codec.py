import json
from collections.abc import Callable
from typing import Any, Literal

from app.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
    SimpleDecisionTrace,
)
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator
from app.domain.visitors.decision_trace_visitor import DecisionTraceVisitor


# ==========
# DecisionTraceDeserializer
# ==========
def _deserialize_composite(data: dict[str, Any]) -> CompositeDecisionTrace:
    return CompositeDecisionTrace(
        result=data["result"],
        operator=LogicalOperator(data["operator"]),
        traces=tuple(_deserialize_dict(data=trace) for trace in data["traces"]),
    )


def _deserialize_simple(data: dict[str, Any]) -> SimpleDecisionTrace:
    return SimpleDecisionTrace(
        result=data["result"],
        operator=ComparisonOperator(data["operator"]),
        field=EventField(data["field"]),
        expected_value=data["expected_value"],
        actual_value=data["actual_value"],
    )


_deserializers: dict[
    Literal["composite", "simple"], Callable[[dict[str, Any]], DecisionTrace]
] = {
    "composite": _deserialize_composite,
    "simple": _deserialize_simple,
}


def _deserialize_dict(data: dict[str, Any]) -> DecisionTrace:
    return _deserializers[data["type"]](data)


def deserialize(traces: str) -> tuple[DecisionTrace, ...]:
    data: list[dict[str, Any]] = json.loads(traces)

    return tuple(_deserialize_dict(data=trace) for trace in data)


class DecisionTraceSerializer(DecisionTraceVisitor[dict[str, Any]]):
    def visit_composite(self, element: CompositeDecisionTrace) -> dict[str, Any]:
        return {
            "type": "composite",
            "result": element.result,
            "operator": element.operator.value,
            "traces": [t.accept(visitor=self) for t in element.traces],
        }

    def visit_simple(self, element: SimpleDecisionTrace) -> dict[str, Any]:
        return {
            "type": "simple",
            "result": element.result,
            "operator": element.operator.value,
            "field": element.field.value,
            "expected_value": element.expected_value,
            "actual_value": element.actual_value,
        }

    def serialize(self, traces: tuple[DecisionTrace, ...]) -> str:
        return json.dumps([trace.accept(visitor=self) for trace in traces])
