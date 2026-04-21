from typing import Any

from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.sqlalchemy.models.model import Model


class RuleModel(Model):
    __tablename__ = "rules"

    name: Mapped[str] = mapped_column(
        String, nullable=False, index=True, unique=True
    )  # tmp
    condition: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    outcome: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (CheckConstraint("priority >= 0"),)
