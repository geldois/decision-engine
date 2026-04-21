from typing import Any

from app.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
    DecisionTraceRegistry,
    DecisionTraceVisitor,
    SimpleDecisionTrace,
)


class DecisionTraceDeserializer:
    @staticmethod
    def deserialize(data: list[dict[str, Any]]) -> tuple[DecisionTrace, ...]:
        return tuple(
            DecisionTraceRegistry.get_class(name=trace["type"]).from_dict(data=trace)
            for trace in data
        )


class DecisionTraceSerializer(DecisionTraceVisitor[dict[str, Any]]):
    @classmethod
    def visit_composite(cls, element: CompositeDecisionTrace) -> dict[str, Any]:
        return {
            "type": "composite",
            "result": element.result,
            "operator": element.operator.value,
            "traces": [t.accept(visitor=cls) for t in element.traces],
        }

    @classmethod
    def visit_simple(cls, element: SimpleDecisionTrace) -> dict[str, Any]:
        return {
            "type": "simple",
            "result": element.result,
            "operator": element.operator.value,
            "field": element.field.value,
            "expected_value": element.expected_value,
            "actual_value": element.actual_value,
        }

    @classmethod
    def serialize(cls, traces: tuple[DecisionTrace, ...]) -> list[dict[str, Any]]:
        return [trace.accept(visitor=cls) for trace in traces]
