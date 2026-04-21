from collections.abc import Callable

from app.domain.entities.event import Event
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_event_repository import (
    SQLAlchemyEventRepository,
)

# VALID CASES


def test_sql_event_repository_returns_saved_event(
    event_factory: Callable[..., Event],
    sqlalchemy_event_repo: SQLAlchemyEventRepository,
) -> None:
    event = event_factory()

    saved = sqlalchemy_event_repo.save(event=event)

    assert saved is event


def test_sql_event_repository_returns_event_when_id_exists(
    event_factory: Callable[..., Event],
    sqlalchemy_event_repo: SQLAlchemyEventRepository,
) -> None:
    event = event_factory()

    sqlalchemy_event_repo.save(event=event)

    returned = sqlalchemy_event_repo.get_by_id(event_id=event.id)

    assert returned

    assert returned == event

    assert returned.is_structurally_equal(other=event)


def test_sql_event_repository_returns_none_when_id_does_not_exist(
    event_factory: Callable[..., Event],
    sqlalchemy_event_repo: SQLAlchemyEventRepository,
) -> None:
    event = event_factory()

    returned = sqlalchemy_event_repo.get_by_id(event_id=event.id)

    assert returned is None


def test_sql_event_repository_returns_true_when_event_is_deleted(
    event_factory: Callable[..., Event],
    sqlalchemy_event_repo: SQLAlchemyEventRepository,
) -> None:
    event = event_factory()

    sqlalchemy_event_repo.save(event=event)

    it_was_deleted = sqlalchemy_event_repo.delete(event=event)

    returned = sqlalchemy_event_repo.get_by_id(event_id=event.id)

    assert it_was_deleted

    assert returned is None


def test_sql_event_repository_returns_false_when_event_is_not_deleted(
    event_factory: Callable[..., Event],
    sqlalchemy_event_repo: SQLAlchemyEventRepository,
) -> None:
    event = event_factory()

    it_was_deleted = sqlalchemy_event_repo.delete(event=event)

    assert not it_was_deleted


def test_sql_event_repository_returns_list_of_rules(
    event_factory: Callable[..., Event],
    sqlalchemy_event_repo: SQLAlchemyEventRepository,
) -> None:
    event = event_factory()

    sqlalchemy_event_repo.save(event=event)

    events = sqlalchemy_event_repo.list_all()

    assert events

    assert isinstance(events, list)

    assert event in events
