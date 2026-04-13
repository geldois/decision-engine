from typing import Any

from app.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
    SimpleDecisionTrace,
)
from app.domain.visitors.decision_trace_visitor import DecisionTraceVisitor


class DecisionTracePresenter(DecisionTraceVisitor[dict[str, Any]]):
    def visit_composite(self, element: CompositeDecisionTrace) -> dict[str, Any]:
        return {
            "type": "composite",
            "result": element.result,
            "operator": element.operator.value,
            "traces": [trace.accept(visitor=self) for trace in element.traces],
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

    def present(self, element: tuple[DecisionTrace, ...]) -> list[dict[str, Any]]:
        return [trace.accept(visitor=self) for trace in element]
