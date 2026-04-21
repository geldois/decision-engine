from typing import Any

from app.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
    DecisionTraceVisitor,
    SimpleDecisionTrace,
)


class DecisionTracePresenter(DecisionTraceVisitor[dict[str, Any]]):
    @classmethod
    def visit_composite(cls, element: CompositeDecisionTrace) -> dict[str, Any]:
        return {
            "type": "composite",
            "result": element.result,
            "operator": element.operator.value,
            "traces": [trace.accept(visitor=cls) for trace in element.traces],
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
    def present(cls, element: tuple[DecisionTrace, ...]) -> list[dict[str, Any]]:
        return [trace.accept(visitor=cls) for trace in element]
