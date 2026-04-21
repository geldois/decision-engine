from collections.abc import Callable
from typing import Any

import pytest

from app.domain.entities.rule import Rule
from app.domain.value_objects.condition import Condition, SimpleCondition
from app.domain.value_objects.decision_outcome import DecisionOutcome


@pytest.fixture(scope="function")
def rule_factory(
    simple_condition_factory: Callable[..., SimpleCondition],
) -> Callable[..., Rule]:
    def _rule_factory(
        *,
        name: str = "TEST",
        condition: Condition | None = None,
        outcome: DecisionOutcome = DecisionOutcome.APPROVED,
        priority: int = 0,
        **overrides: Any,
    ):
        if condition is None:
            condition = simple_condition_factory()

        return Rule(
            name=name,
            condition=condition,
            outcome=outcome,
            priority=priority,
            **overrides,
        )

    return _rule_factory
