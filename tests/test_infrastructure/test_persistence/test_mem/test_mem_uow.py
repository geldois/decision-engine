from collections.abc import Callable

from decision_engine.domain.entities.decision import Decision
from decision_engine.domain.entities.event import Event
from decision_engine.domain.entities.rule import Rule
from decision_engine.infrastructure.persistence.mem.mem_uow import (
    MemUoW,
)

# VALID CASES


def test_mem_uow_commits(
    decision_factory: Callable[..., Decision],
    event_factory: Callable[..., Event],
    rule_factory: Callable[..., Rule],
    mem_uow_factory: Callable[[], MemUoW],
) -> None:
    event = event_factory()
    rule = rule_factory()
    decision = decision_factory(event=event, rules=[rule])

    with mem_uow_factory() as uow:
        uow.events.save(event=event)
        uow.rules.save(rule=rule)
        uow.decisions.save(decision=decision)

    with mem_uow_factory() as uow:
        assert uow.decisions.get_by_id(decision_id=decision.id)
        assert uow.events.get_by_id(event_id=event.id)
        assert uow.rules.get_by_id(rule_id=rule.id)


# INVALID CASES


def test_mem_uow_rolls_back(
    decision_factory: Callable[..., Decision],
    event_factory: Callable[..., Event],
    rule_factory: Callable[..., Rule],
    mem_uow_factory: Callable[[], MemUoW],
) -> None:
    event = event_factory()
    rule = rule_factory()
    decision = decision_factory(event=event, rules=[rule])

    try:
        with mem_uow_factory() as uow:
            uow.events.save(event=event)
            uow.rules.save(rule=rule)
            uow.decisions.save(decision=decision)

            raise Exception
    except Exception:
        pass

    with mem_uow_factory() as uow:
        assert uow.decisions.get_by_id(decision_id=decision.id) is None
        assert uow.events.get_by_id(event_id=event.id) is None
        assert uow.rules.get_by_id(rule_id=rule.id) is None
