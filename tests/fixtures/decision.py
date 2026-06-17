from collections.abc import Callable

import pytest

from decision_engine.domain.entities.decision import Decision
from decision_engine.domain.entities.event import Event
from decision_engine.domain.entities.rule import Rule
from decision_engine.domain.services.decision_engine import DecisionEngine


@pytest.fixture(scope="function")
def decision_factory() -> Callable[..., Decision]:
    def _decision_factory(*, event: Event, rules: list[Rule]) -> Decision:
        return DecisionEngine.decide(event=event, rules=rules)

    return _decision_factory
