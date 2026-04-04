import json
from datetime import UTC
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.contracts.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.domain.entities.event import Event
from app.infrastructure.database.models.event_model import EventModel


class SqlEventRepository(EventRepositoryContract):
    def __init__(self, session: Session) -> None:
        self.session = session

    def convert_event_model_to_event(self, event_model: EventModel) -> Event:
        created_at = (
            event_model.created_at.replace(tzinfo=UTC)
            if event_model.created_at.tzinfo is None
            else event_model.created_at
        )

        event = Event(
            event_type=event_model.event_type,
            payload=json.loads(event_model.payload),
            occurred_at=event_model.occurred_at,
            created_at=created_at,
            event_id=event_model.id,
        )

        return event

    def convert_event_to_event_model(self, event: Event) -> EventModel:
        event_model = EventModel(
            id=event.id,
            event_type=event.event_type,
            payload=json.dumps(event.payload),
            occurred_at=event.occurred_at,
            created_at=event.created_at,
        )

        return event_model

    def save(self, event: Event) -> Event:
        event_model = self.convert_event_to_event_model(event=event)
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
            return self.convert_event_model_to_event(event_model=event_model)

        return None

    def list_all(self) -> list[Event]:
        event_models = self.session.query(EventModel).all()
        events: list[Event] = []

        for event_model in event_models:
            event = self.convert_event_model_to_event(event_model=event_model)
            events.append(event)

        return events
