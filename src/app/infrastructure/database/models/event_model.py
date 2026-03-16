import uuid

from sqlalchemy import JSON, UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[str] = mapped_column(JSON, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
