from utils.domain_entity_util import compare_domain_entities

from app.bootstrap.bootstrap import build_dev_session_factory
from app.domain.entities.events.event import Event
from app.infrastructure.persistence.sql.repositories.sql_event_repository import (
    SqlEventRepository,
)


# ==========
# valid
# ==========
def test_sql_event_repository_returns_saved_event():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    session_factory = build_dev_session_factory()
    event_repository = SqlEventRepository(session=session_factory())

    saved_event = event_repository.save(event=event)

    assert saved_event is event


def test_sql_event_repository_returns_event_when_id_exists():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    session_factory = build_dev_session_factory()
    event_repository = SqlEventRepository(session=session_factory())
    event_repository.save(event=event)

    returned_event = event_repository.get_by_id(event_id=event.id)

    assert compare_domain_entities(a=returned_event, b=event)


def test_sql_event_repository_returns_none_when_id_does_not_exist():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    session_factory = build_dev_session_factory()
    event_repository = SqlEventRepository(session=session_factory())

    returned_event = event_repository.get_by_id(event_id=event.id)

    assert not returned_event


def test_sql_event_repository_returns_true_when_event_is_deleted():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    session_factory = build_dev_session_factory()
    event_repository = SqlEventRepository(session=session_factory())
    event_repository.save(event=event)

    it_was_deleted = event_repository.delete(event=event)

    returned_event = event_repository.get_by_id(event_id=event.id)

    assert it_was_deleted

    assert not returned_event


def test_sql_event_repository_returns_false_when_event_is_not_deleted():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    session_factory = build_dev_session_factory()
    event_repository = SqlEventRepository(session=session_factory())

    it_was_deleted = event_repository.delete(event=event)

    assert not it_was_deleted


def test_sql_event_repository_returns_list_of_rules():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    session_factory = build_dev_session_factory()
    event_repository = SqlEventRepository(session=session_factory())
    event_repository.save(event=event)

    events = event_repository.list_all()

    assert events

    assert isinstance(events, list)

    for e in events:
        if e.id == event.id:
            assert compare_domain_entities(a=e, b=event)
