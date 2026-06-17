from __future__ import annotations

from decision_engine.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
    DecisionTraceRegistry,
    DecisionTraceVisitor,
    SimpleDecisionTrace,
)


class DecisionTraceDeserializer:
    @staticmethod
    def deserialize(data: list[dict[str, object]]) -> tuple[DecisionTrace, ...]:
        return tuple(
            DecisionTraceRegistry.get_class(name=trace["type"]).from_dict(data=trace)
            for trace in data
        )


class DecisionTraceSerializer(DecisionTraceVisitor[dict[str, object]]):
    @classmethod
    def visit_composite(cls, element: CompositeDecisionTrace) -> dict[str, object]:
        return {
            "type": "composite",
            "result": element.result,
            "operator": element.operator.value,
            "traces": [t.accept(visitor=cls) for t in element.traces],
        }

    @classmethod
    def visit_simple(cls, element: SimpleDecisionTrace) -> dict[str, object]:
        return {
            "type": "simple",
            "result": element.result,
            "operator": element.operator.value,
            "field": element.field.value,
            "expected_value": element.expected_value,
            "actual_value": element.actual_value,
        }

    @classmethod
    def serialize(cls, traces: tuple[DecisionTrace, ...]) -> list[dict[str, object]]:
        return [trace.accept(visitor=cls) for trace in traces]
