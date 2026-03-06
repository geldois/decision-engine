from sqlalchemy.orm import Session
import json

from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.domain.events.event import Event
from app.infrastructure.database.models import EventModel

class SqlEventRepository(EventRepositoryContract):
    # initializer
    def __init__(
        self, 
        session: Session
    ):
        self.session = session

    # methods

    # interface methods
    def save(
        self, 
        event: Event
    ) -> Event:
        event_model = EventModel(
            event_type = event.event_type, 
            payload = json.dumps(event.payload), 
            timestamp = event.timestamp
        )
        self.session.add(event_model)
        self.session.flush()
        self.session.refresh(event_model)
        event.event_id = event_model.event_id

        return event
        