import app.infrastructure.serialization.decision_trace_codec as DecisionTraceCodec
from app.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    SimpleDecisionTrace,
)
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator


# ==========
# valid cases
# ==========
def test_decision_trace_codec_serializes_simple_tuple_of_decision_traces() -> None:
    traces = (
        SimpleDecisionTrace(
            result=False,
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            expected_value="USER_CREATED",
            actual_value="TEST",
        ),
    )

    data = DecisionTraceCodec.DecisionTraceSerializer().serialize(traces=traces)

    assert (
        data
        == '[{"type": "simple", "result": false, "operator": "==", "field": "event_type", "expected_value": "USER_CREATED", "actual_value": "TEST"}]'
    )


def test_decision_trace_codec_deserializes_simple_tuple_of_decision_traces() -> None:
    traces = (
        SimpleDecisionTrace(
            result=True,
            operator=ComparisonOperator.EQUALS,
            field=EventField.EVENT_TYPE,
            expected_value="USER_CREATED",
            actual_value="TEST",
        ),
    )

    data = DecisionTraceCodec.DecisionTraceSerializer().serialize(traces=traces)

    assert DecisionTraceCodec.deserialize(traces=data) == traces


def test_decision_trace_codec_serializes_composite_tuple_of_decision_traces() -> None:
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

    data = DecisionTraceCodec.DecisionTraceSerializer().serialize(traces=traces)

    assert (
        data
        == '[{"type": "composite", "result": false, "operator": "and", "traces": [{"type": "simple", "result": false, "operator": "==", "field": "event_type", "expected_value": "USER_CREATED", "actual_value": "TEST"}, {"type": "simple", "result": false, "operator": "==", "field": "event_type", "expected_value": "USER_CREATED", "actual_value": "TEST"}]}, {"type": "simple", "result": false, "operator": "==", "field": "event_type", "expected_value": "USER_CREATED", "actual_value": "TEST"}]'
    )


def test_decision_trace_codec_deserializes_composite_tuple_of_decision_traces() -> None:
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

    data = DecisionTraceCodec.DecisionTraceSerializer().serialize(traces=traces)

    assert DecisionTraceCodec.deserialize(traces=data) == traces
