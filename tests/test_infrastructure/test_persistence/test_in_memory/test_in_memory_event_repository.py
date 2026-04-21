from collections.abc import Callable

from app.domain.entities.event import Event
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)

# VALID CASES


def test_in_memory_event_repository_returns_saved_event(
    event_factory: Callable[..., Event],
    in_memory_event_repo: InMemoryEventRepository,
) -> None:
    event = event_factory()

    saved = in_memory_event_repo.save(event=event)

    assert saved is event


def test_in_memory_event_repository_returns_event_when_id_exists(
    event_factory: Callable[..., Event],
    in_memory_event_repo: InMemoryEventRepository,
) -> None:
    event = event_factory()

    in_memory_event_repo.save(event=event)

    returned = in_memory_event_repo.get_by_id(event_id=event.id)

    assert returned is event


def test_in_memory_event_repository_returns_none_when_id_does_not_exist(
    event_factory: Callable[..., Event],
    in_memory_event_repo: InMemoryEventRepository,
) -> None:
    event = event_factory()

    returned = in_memory_event_repo.get_by_id(event_id=event.id)

    assert returned is None


def test_in_memory_event_repository_returns_true_when_event_is_deleted(
    event_factory: Callable[..., Event],
    in_memory_event_repo: InMemoryEventRepository,
) -> None:
    event = event_factory()

    in_memory_event_repo.save(event=event)

    it_was_deleted = in_memory_event_repo.delete(event=event)

    returned = in_memory_event_repo.get_by_id(event_id=event.id)

    assert it_was_deleted

    assert returned is None


def test_in_memory_event_repository_returns_false_when_event_is_not_deleted(
    event_factory: Callable[..., Event],
    in_memory_event_repo: InMemoryEventRepository,
) -> None:
    event = event_factory()

    it_was_deleted = in_memory_event_repo.delete(event=event)

    assert not it_was_deleted


def test_in_memory_event_repository_returns_list_of_events(
    event_factory: Callable[..., Event],
    in_memory_event_repo: InMemoryEventRepository,
) -> None:
    event = event_factory()

    in_memory_event_repo.save(event=event)

    events = in_memory_event_repo.list_all()

    assert isinstance(events, list)

    assert event in events
