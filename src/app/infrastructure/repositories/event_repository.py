from app.domain.events.event import Event

class EventRepository:
    # constructor
    def __init__(self):
        self._next_id = 1
        self._events = {}
    # methods
    def save(self, event: Event):
        if event.event_id is None:
            event.event_id = self._next_id
            self._next_id += 1
            self._events[event.event_id] = event
        return event
    def get_by_id(self, event_id: int):
        return self._events.get(event_id, None)
    