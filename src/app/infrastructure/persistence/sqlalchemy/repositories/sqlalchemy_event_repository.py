from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.contracts.repository import EventRepository
from app.domain.entities.event import Event
from app.infrastructure.persistence.sqlalchemy.mappers.sqlalchemy_event_mapper import (
    domain_to_model,
    model_to_domain,
)
from app.infrastructure.persistence.sqlalchemy.models.event_model import EventModel


class SQLAlchemyEventRepository(EventRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, event: Event) -> Event:
        event_model = domain_to_model(event=event)
        self.session.add(event_model)
        self.session.flush()
        self.session.refresh(event_model)

        return event

    def delete(self, event: Event) -> bool:
        event_model = (
            self.session.execute(select(EventModel).where(EventModel.id == event.id))
            .scalars()
            .first()
        )

        if event_model:
            self.session.delete(event_model)
            self.session.flush()

            return True

        return False

    def get_by_id(self, event_id: UUID) -> Event | None:
        event_model = (
            self.session.execute(select(EventModel).where(EventModel.id == event_id))
            .scalars()
            .first()
        )

        if event_model:
            return model_to_domain(event_model=event_model)

        return None

    def list_all(self) -> list[Event]:
        event_models = self.session.query(EventModel).all()
        events: list[Event] = []

        for event_model in event_models:
            event = model_to_domain(event_model=event_model)
            events.append(event)

        return events
