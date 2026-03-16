import uuid

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base


class DecisionModel(Base):
    __tablename__ = "decisions"

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("events._id"), nullable=False
    )
    rule_id: Mapped[uuid.UUID] = mapped_column(
        UUID, ForeignKey("rules._id"), nullable=True
    )
    outcome: Mapped[str] = mapped_column(String, nullable=False)
    explanation: Mapped[str] = mapped_column(String, nullable=False)

    event = relationship("EventModel")
    rule = relationship("RuleModel")
