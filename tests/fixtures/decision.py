from collections.abc import Callable

import pytest

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.services.decision_engine import DecisionEngine


@pytest.fixture(scope="function")
def decision_factory() -> Callable[..., Decision]:
    def _decision_factory(*, event: Event, rules: list[Rule]) -> Decision:
        return DecisionEngine.decide(event=event, rules=rules)

    return _decision_factory
