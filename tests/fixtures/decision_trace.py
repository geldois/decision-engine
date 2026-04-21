from collections.abc import Callable

import pytest

from app.domain.value_objects.decision_trace import SimpleDecisionTrace
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


@pytest.fixture(scope="function")
def simple_decision_trace_factory() -> Callable[..., SimpleDecisionTrace]:
    def _simple_decision_trace(
        result: bool = False,
        operator: ComparisonOperator = ComparisonOperator.EQUALS,
        field: EventField = EventField.EVENT_TYPE,
        expected_value: object = "USER_CREATED",
        actual_value: object = "TEST",
    ) -> SimpleDecisionTrace:
        return SimpleDecisionTrace(
            result=result,
            operator=operator,
            field=field,
            expected_value=expected_value,
            actual_value=actual_value,
        )

    return _simple_decision_trace
