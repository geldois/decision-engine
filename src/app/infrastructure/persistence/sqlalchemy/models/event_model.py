from typing import Any

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.sqlalchemy.models.model import Model


class EventModel(Model):
    __tablename__ = "events"

    event_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    occurred_at: Mapped[int] = mapped_column(Integer, nullable=False, index=True)  # tmp
