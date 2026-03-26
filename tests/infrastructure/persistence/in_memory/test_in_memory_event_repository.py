from app.domain.entities.event import Event
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


# ==========
# valid
# ==========
def test_in_memory_event_repository_returns_saved_event():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    event_repository = InMemoryEventRepository(in_memory_storage=InMemoryStorage())

    saved_event = event_repository.save(event=event)

    assert saved_event is event


def test_in_memory_event_repository_returns_event_when_id_exists():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    event_repository = InMemoryEventRepository(in_memory_storage=InMemoryStorage())
    event_repository.save(event=event)

    returned_event = event_repository.get_by_id(event_id=event.id)

    assert returned_event is event


def test_in_memory_event_repository_returns_none_when_id_does_not_exist():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    event_repository = InMemoryEventRepository(in_memory_storage=InMemoryStorage())

    returned_event = event_repository.get_by_id(event_id=event.id)

    assert not returned_event


def test_in_memory_event_repository_returns_true_when_event_is_deleted():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    event_repository = InMemoryEventRepository(in_memory_storage=InMemoryStorage())
    event_repository.save(event=event)

    it_was_deleted = event_repository.delete(event=event)

    returned_event = event_repository.get_by_id(event_id=event.id)

    assert it_was_deleted

    assert not returned_event


def test_in_memory_event_repository_returns_false_when_event_is_not_deleted():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    event_repository = InMemoryEventRepository(in_memory_storage=InMemoryStorage())

    it_was_deleted = event_repository.delete(event=event)

    assert not it_was_deleted


def test_in_memory_event_repository_returns_list_of_events():
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    event_repository = InMemoryEventRepository(in_memory_storage=InMemoryStorage())
    event_repository.save(event=event)

    events = event_repository.list_all()

    assert isinstance(events, list)

    assert event in events
