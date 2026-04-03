from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class RuleModel(Base):
    __tablename__ = "rules"

    name: Mapped[str] = mapped_column(String, nullable=False)
    condition_field: Mapped[str] = mapped_column(String, nullable=False)
    condition_operator: Mapped[str] = mapped_column(String, nullable=False)
    condition_value_int: Mapped[int] = mapped_column(Integer, nullable=True)
    condition_value_str: Mapped[str] = mapped_column(String, nullable=True)
    outcome: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("condition_operator IN ('==', '!=', '<', '>')"),
        CheckConstraint(
            "(condition_value_int IS NULL OR condition_value_str IS NULL) \
            AND \
            (condition_value_int IS NOT NULL OR condition_value_str IS NOT NULL)"
        ),
        CheckConstraint("priority >= 0"),
    )
