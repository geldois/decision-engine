from app.domain.entities.event import Event
from app.infrastructure.persistence.sqlalchemy.codecs.payload_codec import (
    PayloadDeserializer,
    PayloadSerializer,
)
from app.infrastructure.persistence.sqlalchemy.models.event_model import EventModel


def domain_to_model(event: Event) -> EventModel:
    event_model = EventModel(
        id=event.id,
        event_type=event.event_type,
        payload=PayloadSerializer.serialize(payload=event.payload),
        occurred_at=event.occurred_at,
        created_at=event.created_at,
    )

    return event_model


def model_to_domain(event_model: EventModel) -> Event:
    event = Event(
        event_type=event_model.event_type,
        payload=PayloadDeserializer.deserialize(data=event_model.payload),
        occurred_at=event_model.occurred_at,
        created_at=event_model.created_at,
        event_id=event_model.id,
    )

    return event
