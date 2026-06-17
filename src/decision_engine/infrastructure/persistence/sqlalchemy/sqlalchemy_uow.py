from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.application.contracts.uow import UoW
from decision_engine.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_decision_repository import (  # noqa: E501
    SQLAlchemyDecisionRepository,
)
from decision_engine.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_event_repository import (  # noqa: E501
    SQLAlchemyEventRepository,
)
from decision_engine.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_rule_repository import (  # noqa: E501
    SQLAlchemyRuleRepository,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from sqlalchemy.orm import Session


class SQLAlchemyUoW(UoW):
    def __init__(self, *, session_factory: Callable[[], Session]) -> None:
        self.session_factory = session_factory

    def __enter__(self) -> UoW:
        self.session = self.session_factory()

        self.decisions = SQLAlchemyDecisionRepository(session=self.session)
        self.events = SQLAlchemyEventRepository(session=self.session)
        self.rules = SQLAlchemyRuleRepository(session=self.session)

        return super().__enter__()

    def commit(self) -> None:
        self.session.commit()
        self.session.close()

    def rollback(self) -> None:
        self.session.rollback()
        self.session.close()
