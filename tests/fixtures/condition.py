from collections.abc import Callable
from typing import Any

import pytest

from app.domain.value_objects.condition import SimpleCondition
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


@pytest.fixture(scope="function")
def simple_condition_factory() -> Callable[..., SimpleCondition]:
    def _simple_condition_factory(
        *,
        operator: ComparisonOperator = ComparisonOperator.EQUALS,
        field: EventField = EventField.EVENT_TYPE,
        value: Any = "TEST",
    ) -> SimpleCondition:
        return SimpleCondition(operator=operator, field=field, value=value)

    return _simple_condition_factory
