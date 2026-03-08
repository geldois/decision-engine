import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.engine import Base

class EventModel(Base):
    __tablename__ = "events"

    _id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key = True)
    event_type: Mapped[str] = mapped_column(String, nullable = False)
    payload: Mapped[str] = mapped_column(String, nullable = False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable = False)

class RuleModel(Base):
    __tablename__ = "rules"

    _id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key = True)
    name: Mapped[str] = mapped_column(String, nullable = False)
    condition_field: Mapped[str] = mapped_column(String, nullable = False)
    condition_operator: Mapped[str] = mapped_column(String, nullable = False)
    condition_value_int: Mapped[int] = mapped_column(Integer, nullable = True)
    condition_value_str: Mapped[str] = mapped_column(String, nullable = True)
    outcome: Mapped[str] = mapped_column(String, nullable = False)

    __table_args__ = (
        CheckConstraint(
            "condition_operator IN ('==', '!=', '<', '>')"
        ), 
        CheckConstraint(
            "(condition_value_int IS NULL OR condition_value_str IS NULL) AND (condition_value_int IS NOT NULL OR condition_value_str IS NOT NULL)"
        )
    )

class DecisionModel(Base):
    __tablename__ = "decisions"

    _id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key = True)
    event_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("events._id"), nullable = False)
    rule_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("rules._id"), nullable = True)
    outcome: Mapped[str] = mapped_column(String, nullable = False)
    explanation: Mapped[str] = mapped_column(String, nullable = False)

    event = relationship("EventModel")
    rule = relationship("RuleModel")
