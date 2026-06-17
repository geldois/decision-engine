from collections.abc import Callable

from decision_engine.domain.entities.decision import Decision
from decision_engine.domain.entities.event import Event
from decision_engine.domain.entities.rule import Rule
from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage

# VALID CASES


def test_mem_storage_creates_empty_dicts() -> None:
    storage = MemStorage()

    assert storage.decisions == {}

    assert storage.events == {}

    assert storage.rules == {}


def test_mem_storage_creates_new_dict_when_backups(
    make_decision: Callable[..., Decision],
    make_event: Callable[..., Event],
    make_rule: Callable[..., Rule],
) -> None:
    storage = MemStorage()

    event = make_event()
    rule = make_rule()
    decision = make_decision(event=event, rules=[rule])

    storage.decisions = {decision.id: decision}
    storage.events = {event.id: event}
    storage.rules = {rule.id: rule}

    storage_backup = storage.backup()

    assert storage_backup.decisions is not storage.decisions

    assert storage_backup.events is not storage.events

    assert storage_backup.rules is not storage.rules

    assert storage_backup.decisions == storage.decisions

    assert storage_backup.events == storage.events

    assert storage_backup.rules == storage.rules


def test_mem_storage_cleans_storage() -> None:
    storage = MemStorage()

    storage.clear()

    assert storage.decisions == {}

    assert storage.events == {}

    assert storage.rules == {}


def test_mem_storage_updates_storage(
    make_decision: Callable[..., Decision],
    make_event: Callable[..., Event],
    make_rule: Callable[..., Rule],
) -> None:
    storage = MemStorage()
    new_storage = MemStorage()

    event = make_event()
    rule = make_rule()
    decision = make_decision(event=event, rules=[rule])

    new_storage.decisions = {decision.id: decision}
    new_storage.events = {event.id: event}
    new_storage.rules = {rule.id: rule}

    storage.update(new_storage=new_storage)

    assert new_storage.decisions is not storage.decisions

    assert new_storage.events is not storage.events

    assert new_storage.rules is not storage.rules

    for d in new_storage.decisions:
        assert d in storage.decisions

    for e in new_storage.events:
        assert e in storage.events

    for r in new_storage.rules:
        assert r in storage.rules
