from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

import app.infrastructure.persistence.sql.mappers.sql_event_mapper as SQLEventMapper
from app.application.contracts.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.domain.entities.event import Event
from app.infrastructure.database.models.event_model import EventModel


class SQLEventRepository(EventRepositoryContract):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, event: Event) -> Event:
        event_model = SQLEventMapper.domain_to_model(event=event)
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
            return SQLEventMapper.model_to_domain(event_model=event_model)

        return None

    def list_all(self) -> list[Event]:
        event_models = self.session.query(EventModel).all()
        events: list[Event] = []

        for event_model in event_models:
            event = SQLEventMapper.model_to_domain(event_model=event_model)
            events.append(event)

        return events
