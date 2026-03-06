from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.engine import Base

class EventModel(Base):
    __tablename__ = "events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key = True)
    event_type: Mapped[str] = mapped_column(String, nullable = False)
    payload: Mapped[str] = mapped_column(String, nullable = False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable = False)

class RuleModel(Base):
    __tablename__ = "rules"

    rule_id: Mapped[int] = mapped_column(Integer, primary_key = True)
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
