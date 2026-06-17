from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from decision_engine.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
)
from decision_engine.domain.value_objects.operators.logical_operator import (
    LogicalOperator,
)
from decision_engine.infrastructure.persistence.sqlalchemy.codecs.decision_trace_codec import (  # noqa: E501
    DecisionTraceDeserializer,
    DecisionTraceSerializer,
)

if TYPE_CHECKING:
    from tests.conftest import MakeSimpleDecisionTrace


@pytest.fixture
def decision_traces(
    make_simple_decision_trace: MakeSimpleDecisionTrace,
) -> tuple[DecisionTrace, ...]:
    return (
        CompositeDecisionTrace(
            result=False,
            operator=LogicalOperator.AND,
            traces=(
                make_simple_decision_trace(),
                make_simple_decision_trace(),
            ),
        ),
        make_simple_decision_trace(),
    )


# VALID CASES


def test_decision_trace_codec_roundtrip_preserves_structure(
    decision_traces: tuple[DecisionTrace, ...],
) -> None:
    encoded = DecisionTraceSerializer.serialize(traces=decision_traces)
    decoded = DecisionTraceDeserializer.deserialize(data=encoded)

    assert decoded == decision_traces
