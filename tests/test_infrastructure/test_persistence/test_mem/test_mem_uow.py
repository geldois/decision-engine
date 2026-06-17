from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Callable

    from decision_engine.infrastructure.persistence.mem.mem_uow import MemUoW
    from tests.conftest import MakeDecision, MakeEvent, MakeRule

# VALID CASES


def test_mem_uow_commits(
    make_decision: MakeDecision,
    make_event: MakeEvent,
    make_rule: MakeRule,
    mem_uow_factory: Callable[[], MemUoW],
) -> None:
    event = make_event()
    rule = make_rule()
    decision = make_decision(event=event, rules=[rule])

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
    make_decision: MakeDecision,
    make_event: MakeEvent,
    make_rule: MakeRule,
    mem_uow_factory: Callable[[], MemUoW],
) -> None:
    event = make_event()
    rule = make_rule()
    decision = make_decision(event=event, rules=[rule])

    def run_transaction_with_error() -> None:
        with mem_uow_factory() as uow:
            uow.events.save(event=event)
            uow.rules.save(rule=rule)
            uow.decisions.save(decision=decision)

            raise RuntimeError

    with pytest.raises(RuntimeError):
        run_transaction_with_error()

    with mem_uow_factory() as uow:
        assert uow.decisions.get_by_id(decision_id=decision.id) is None
        assert uow.events.get_by_id(event_id=event.id) is None
        assert uow.rules.get_by_id(rule_id=rule.id) is None
