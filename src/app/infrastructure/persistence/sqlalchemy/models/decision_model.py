import uuid
from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.model import Model


class DecisionModel(Model):
    __tablename__ = "decisions"

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("events.id"), nullable=False, index=True
    )
    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rules.id"), nullable=True, index=True
    )
    outcome: Mapped[str] = mapped_column(String, nullable=False, index=True)
    traces: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False)

    event = relationship("EventModel", lazy="joined")
    rule = relationship("RuleModel", lazy="joined")
