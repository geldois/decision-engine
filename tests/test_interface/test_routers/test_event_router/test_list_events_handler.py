from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from decision_engine.application.use_cases.list_events import ListEventsUseCase

if TYPE_CHECKING:
    from collections.abc import Callable

    from fastapi.testclient import TestClient

    from decision_engine.application.dto.responses.register_event import (
        RegisterEventDTOResponse,
    )
    from decision_engine.config.container import Container


class BrokenListEventsUseCase(ListEventsUseCase):
    def execute(self, dto: None) -> list[RegisterEventDTOResponse]:  # noqa: ARG002
        message = "boom"

        raise RuntimeError(message)


@pytest.fixture
def broken_list_events(container: Container) -> BrokenListEventsUseCase:
    return BrokenListEventsUseCase(uow_factory=container.db.uow_factory)


# VALID CASES


def test_list_events_handler_returns_200_and_empty_list(
    fastapi_testclient: TestClient,
) -> None:
    response = fastapi_testclient.get("/events/")

    assert response.status_code == 200

    assert response.json() == []


def test_list_events_handler_returns_200_and_valid_http_response(
    fastapi_testclient: TestClient,
) -> None:
    event_request = {
        "event_type": "USER_CREATED",
        "payload": {"user_id": 1},
        "occurred_at": 1700000000,
    }

    fastapi_testclient.post("/events/", json=event_request)

    response = fastapi_testclient.get("/events/")

    assert response.status_code == 200

    assert len(response.json()) == 1

    assert response.json()[0]["event_type"] == event_request["event_type"]

    assert response.json()[0]["event_id"]


# INVALID CASES


def test_list_events_handler_returns_500_on_internal_error(
    broken_fastapi_testclient_factory: Callable[..., TestClient],
    broken_list_events: BrokenListEventsUseCase,
) -> None:
    broken_fastapi_testclient = broken_fastapi_testclient_factory(
        list_events=broken_list_events
    )

    response = broken_fastapi_testclient.get("/events/")

    assert response.status_code == 500

    assert response.json()["detail"]
