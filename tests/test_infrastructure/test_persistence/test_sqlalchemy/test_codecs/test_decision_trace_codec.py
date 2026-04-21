from collections.abc import Callable

import pytest

from app.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
    SimpleDecisionTrace,
)
from app.domain.value_objects.operators.logical_operator import LogicalOperator
from app.infrastructure.persistence.sqlalchemy.codecs.decision_trace_codec import (
    DecisionTraceDeserializer,
    DecisionTraceSerializer,
)


@pytest.fixture(scope="function")
def decision_traces(
    simple_decision_trace_factory: Callable[..., SimpleDecisionTrace],
) -> tuple[DecisionTrace, ...]:
    return (
        CompositeDecisionTrace(
            result=False,
            operator=LogicalOperator.AND,
            traces=(
                simple_decision_trace_factory(),
                simple_decision_trace_factory(),
            ),
        ),
        simple_decision_trace_factory(),
    )


# VALID CASES


def test_decision_trace_codec_roundtrip_preserves_structure(
    decision_traces: tuple[DecisionTrace, ...],
) -> None:
    encoded = DecisionTraceSerializer.serialize(traces=decision_traces)
    decoded = DecisionTraceDeserializer.deserialize(data=encoded)

    assert decoded == decision_traces
