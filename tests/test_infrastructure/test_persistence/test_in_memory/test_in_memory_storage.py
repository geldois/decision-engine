from collections.abc import Callable

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage

# VALID CASES


def test_in_memory_storage_creates_empty_dicts() -> None:
    storage = InMemoryStorage()

    assert storage.decisions == {}

    assert storage.events == {}

    assert storage.rules == {}


def test_in_memory_storage_creates_new_dict_when_backups(
    decision_factory: Callable[..., Decision],
    event_factory: Callable[..., Event],
    rule_factory: Callable[..., Rule],
) -> None:
    storage = InMemoryStorage()

    event = event_factory()
    rule = rule_factory()
    decision = decision_factory(event=event, rules=[rule])

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


def test_in_memory_storage_cleans_storage() -> None:
    storage = InMemoryStorage()

    storage.clear()

    assert storage.decisions == {}

    assert storage.events == {}

    assert storage.rules == {}


def test_in_memory_storage_updates_storage(
    decision_factory: Callable[..., Decision],
    event_factory: Callable[..., Event],
    rule_factory: Callable[..., Rule],
) -> None:
    storage = InMemoryStorage()
    new_storage = InMemoryStorage()

    event = event_factory()
    rule = rule_factory()
    decision = decision_factory(event=event, rules=[rule])

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
