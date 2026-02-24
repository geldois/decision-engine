import json

from sqlalchemy.orm import Session

from app.domain.events.event import Event
from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.infrastructure.database.engine import SessionLocal
from app.infrastructure.database.models import EventModel

class SqlEventRepository(EventRepositoryContract):
    # methods
    def save(
        self,
        event: Event
    ) -> Event:
        db: Session = SessionLocal()
        try:
            event_model = EventModel(
                event_type = event.event_type,
                payload = json.dumps(event.payload),
                timestamp = event.timestamp
            )
            db.add(event_model)
            db.commit()
            db.refresh(event_model)
            event.event_id = event_model.id

            return event
        finally:
            db.close()
