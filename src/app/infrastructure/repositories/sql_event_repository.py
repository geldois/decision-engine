from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID
import json

from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.domain.entities.events.event import Event
from app.infrastructure.database.models import EventModel

class SqlEventRepository(EventRepositoryContract):
    # initializer
    def __init__(
        self, 
        session: Session
    ):
        self.session = session

    # methods
    def convert_event_model_to_event(
        self, 
        event_model: EventModel
    ) -> Event:
        event = Event(
            event_type = event_model.event_type, 
            payload = json.loads(event_model.payload), 
            timestamp = event_model.timestamp, 
            event_id = event_model._id
        )
        
        return event
    
    def convert_event_to_event_model(
        self, 
        event: Event
    ) -> EventModel:
        event_model = EventModel(
            _id = event._id, 
            event_type = event.event_type, 
            payload = json.dumps(event.payload), 
            timestamp = event.timestamp
        )

        return event_model

    # interface methods
    def save(
        self, 
        event: Event
    ) -> Event:
        event_model = self.convert_event_to_event_model(event = event)
        self.session.add(event_model)
        self.session.flush()
        self.session.refresh(event_model)

        return event
        
    def delete(
        self, 
        event: Event
    ) -> bool:
        event_model = (
            self.session.execute(
                select(EventModel).where(EventModel._id == event._id)
            )
            .scalars()
            .first()
        )

        if event_model:
            self.session.delete(event_model)

            return True
        
        return False
    
    def get_by_id(
        self, 
        event_id: UUID
    ) -> Event | None:
        event_model = (
            self.session.execute(
                select(EventModel).where(EventModel._id == event_id)
            )
            .scalars()
            .first()
        )

        if event_model:
            return self.convert_event_model_to_event(event_model = event_model)
        
        return None
    
    def list_all(self) -> list[Event]:
        event_models = self.session.query(EventModel).all()
        events = []

        for event_model in event_models:
            event = self.convert_event_model_to_event(event_model = event_model)
            events.append(event)

        return events
    