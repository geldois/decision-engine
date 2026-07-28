from __future__ import annotations

from typing import TYPE_CHECKING, cast

from sqlalchemy.exc import OperationalError

from decision_engine.infrastructure.persistence.sqlalchemy.db import SQLAlchemyDB

if TYPE_CHECKING:
    from collections.abc import Callable

    from sqlalchemy import Engine
    from sqlalchemy.orm import Session

    from decision_engine.infrastructure.persistence.sqlalchemy.sqlalchemy_uow import (
        SQLAlchemyUoW,
    )


def test_check_health_returns_false_when_session_errors() -> None:
    def failing_session_factory() -> Session:
        statement = "SELECT 1"
        message = "database down"

        raise OperationalError(statement, {}, OSError(message))

    db = SQLAlchemyDB(
        uow_factory=cast("Callable[[], SQLAlchemyUoW]", lambda: None),
        database_url="",
        engine=cast("Engine", None),
        session_factory=failing_session_factory,
    )

    assert db.check_health() is False
