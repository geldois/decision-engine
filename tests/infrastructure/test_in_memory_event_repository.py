from app.domain.entities.events.event import Event
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository

# tests
def test_in_memory_event_repository_assigns_correct_id_when_event_is_saved():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    
    saved_event = event_repository.save(event = event)
    
    assert saved_event is event

    assert saved_event._id
    
    assert saved_event._id == event._id

def test_in_memory_event_repository_returns_event_when_id_exists():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event = event)
    
    returned_event = event_repository.get_by_id(event_id = saved_event._id)
    
    assert returned_event is saved_event

def test_in_memory_event_repository_returns_none_when_id_does_not_exist():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    
    returned_event = event_repository.get_by_id(event_id = event._id)
    
    assert not returned_event

def test_in_memory_event_repository_returns_true_when_event_is_deleted():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event = event)

    it_was_deleted = event_repository.delete(event = saved_event)

    returned_event = event_repository.get_by_id(event_id = saved_event._id)

    assert it_was_deleted

    assert not returned_event

def test_in_memory_event_repository_returns_false_when_event_is_not_deleted():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()

    it_was_deleted = event_repository.delete(event = event)

    assert not it_was_deleted

def test_in_memory_rule_repository_returns_a_valid_list_of_rules():
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123,
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event = event)

    events = event_repository.list_all()

    assert events

    assert isinstance(events, list)

    assert saved_event in events
    