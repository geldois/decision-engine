from datetime import UTC

import app.infrastructure.serialization.payload_codec as PayloadCodec
from app.domain.entities.event import Event
from app.infrastructure.database.models.event_model import EventModel


def domain_to_model(event: Event) -> EventModel:
    event_model = EventModel(
        id=event.id,
        event_type=event.event_type,
        payload=PayloadCodec.serialize(event.payload),
        occurred_at=event.occurred_at,
        created_at=event.created_at,
    )

    return event_model


def model_to_domain(event_model: EventModel) -> Event:
    created_at = (
        event_model.created_at.replace(tzinfo=UTC)
        if event_model.created_at.tzinfo is None
        else event_model.created_at
    )

    event = Event(
        event_type=event_model.event_type,
        payload=PayloadCodec.deserialize(event_model.payload),
        occurred_at=event_model.occurred_at,
        created_at=created_at,
        event_id=event_model.id,
    )

    return event
