from collections.abc import Callable

from decision_engine.domain.entities.event import Event
from decision_engine.infrastructure.persistence.mem.repositories.mem_event_repository import (
    MemEventRepository,
)

# VALID CASES


def test_mem_event_repository_returns_saved_event(
    event_factory: Callable[..., Event],
    mem_event_repo: MemEventRepository,
) -> None:
    event = event_factory()

    saved = mem_event_repo.save(event=event)

    assert saved is event


def test_mem_event_repository_returns_event_when_id_exists(
    event_factory: Callable[..., Event],
    mem_event_repo: MemEventRepository,
) -> None:
    event = event_factory()

    mem_event_repo.save(event=event)

    returned = mem_event_repo.get_by_id(event_id=event.id)

    assert returned is event


def test_mem_event_repository_returns_none_when_id_does_not_exist(
    event_factory: Callable[..., Event],
    mem_event_repo: MemEventRepository,
) -> None:
    event = event_factory()

    returned = mem_event_repo.get_by_id(event_id=event.id)

    assert returned is None


def test_mem_event_repository_returns_true_when_event_is_deleted(
    event_factory: Callable[..., Event],
    mem_event_repo: MemEventRepository,
) -> None:
    event = event_factory()

    mem_event_repo.save(event=event)

    it_was_deleted = mem_event_repo.delete(event=event)

    returned = mem_event_repo.get_by_id(event_id=event.id)

    assert it_was_deleted

    assert returned is None


def test_mem_event_repository_returns_false_when_event_is_not_deleted(
    event_factory: Callable[..., Event],
    mem_event_repo: MemEventRepository,
) -> None:
    event = event_factory()

    it_was_deleted = mem_event_repo.delete(event=event)

    assert not it_was_deleted


def test_mem_event_repository_returns_list_of_events(
    event_factory: Callable[..., Event],
    mem_event_repo: MemEventRepository,
) -> None:
    event = event_factory()

    mem_event_repo.save(event=event)

    events = mem_event_repo.list_all()

    assert isinstance(events, list)

    assert event in events
