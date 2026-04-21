from collections.abc import Callable
from typing import Any

import pytest

from app.domain.entities.event import Event


@pytest.fixture(scope="function")
def event_factory() -> Callable[..., Event]:
    def _event_factory(
        *,
        event_type: str = "TEST",
        payload: dict[str, Any] | None = None,
        occurred_at: int = 1000000000,
        **overrides: Any,
    ) -> Event:
        if payload is None:
            payload = {"test": True, "info": "TEST"}

        return Event(
            event_type=event_type, payload=payload, occurred_at=occurred_at, **overrides
        )

    return _event_factory
