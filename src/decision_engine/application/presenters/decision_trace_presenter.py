from __future__ import annotations

from decision_engine.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
    DecisionTraceVisitor,
    SimpleDecisionTrace,
)


class DecisionTracePresenter(DecisionTraceVisitor[dict[str, object]]):
    @classmethod
    def visit_composite(cls, element: CompositeDecisionTrace) -> dict[str, object]:
        return {
            "type": "composite",
            "result": element.result,
            "operator": element.operator.value,
            "traces": [trace.accept(visitor=cls) for trace in element.traces],
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
    def present(cls, element: tuple[DecisionTrace, ...]) -> list[dict[str, object]]:
        return [trace.accept(visitor=cls) for trace in element]
