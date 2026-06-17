from __future__ import annotations

from decision_engine.application.presenters.decision_trace_presenter import (
    DecisionTracePresenter,
)
from decision_engine.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    SimpleDecisionTrace,
)
from decision_engine.domain.value_objects.event_field import EventField
from decision_engine.domain.value_objects.operators.comparison_operator import (
    ComparisonOperator,
)
from decision_engine.domain.value_objects.operators.logical_operator import (
    LogicalOperator,
)

# VALID CASES


def test_decision_trace_presenter_presents_simple_tuple_of_decision_traces() -> None:
    traces = (
        SimpleDecisionTrace(
            result=False,
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            expected_value="USER_CREATED",
            actual_value="TEST",
        ),
    )

    data = DecisionTracePresenter.present(element=traces)

    assert data == [
        {
            "type": "simple",
            "result": False,
            "operator": "==",
            "field": "event_type",
            "expected_value": "USER_CREATED",
            "actual_value": "TEST",
        }
    ]


def test_decision_trace_presenter_presents_composite_tuple_of_decision_traces() -> None:
    traces = (
        CompositeDecisionTrace(
            result=False,
            operator=LogicalOperator.AND,
            traces=(
                SimpleDecisionTrace(
                    result=False,
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    expected_value="USER_CREATED",
                    actual_value="TEST",
                ),
                SimpleDecisionTrace(
                    result=False,
                    operator=ComparisonOperator.EQUALS,
                    field=EventField.EVENT_TYPE,
                    expected_value="USER_CREATED",
                    actual_value="TEST",
                ),
            ),
        ),
        SimpleDecisionTrace(
            result=False,
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            expected_value="USER_CREATED",
            actual_value="TEST",
        ),
    )

    data = DecisionTracePresenter.present(element=traces)

    assert data == [
        {
            "type": "composite",
            "result": False,
            "operator": "and",
            "traces": [
                {
                    "type": "simple",
                    "result": False,
                    "operator": "==",
                    "field": "event_type",
                    "expected_value": "USER_CREATED",
                    "actual_value": "TEST",
                },
                {
                    "type": "simple",
                    "result": False,
                    "operator": "==",
                    "field": "event_type",
                    "expected_value": "USER_CREATED",
                    "actual_value": "TEST",
                },
            ],
        },
        {
            "type": "simple",
            "result": False,
            "operator": "==",
            "field": "event_type",
            "expected_value": "USER_CREATED",
            "actual_value": "TEST",
        },
    ]
