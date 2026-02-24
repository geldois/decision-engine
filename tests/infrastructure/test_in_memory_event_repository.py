from app.domain.events.event import Event
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository

# tests
def test_event_repository_assigns_id_when_event_is_saved():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    event = Event(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
    )
    event_repository = InMemoryEventRepository()
    
    saved_event = event_repository.save(event)
    
    assert saved_event.event_id is not None
    
    assert saved_event.event_id == event.event_id

def test_event_repository_returns_event_when_id_exists():
    event_type = "USER_CREATED"
    payload = {
        "user_id": 123,
        "email": "user@email.com"
    }
    timestamp = 1700000000
    event = Event(
        event_type = event_type, 
        payload = payload, 
        timestamp = timestamp
        )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event)
    
    returned_event = event_repository.get_by_id(saved_event.event_id)
    
    assert returned_event == saved_event
