from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.application.dto.dto_register_event_response import DTORegisterEventResponse
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.config.container import Container


class BrokenRegisterEventUseCase(RegisterEventUseCase):
    def execute(self, dto: DTORegisterEventRequest) -> DTORegisterEventResponse:
        raise RuntimeError("boom")


@pytest.fixture(scope="function")
def broken_register_event(container: Container) -> BrokenRegisterEventUseCase:
    return BrokenRegisterEventUseCase(uow_factory=container.db.uow_factory)


# VALID CASES


def test_register_event_handler_returns_200_and_valid_http_response(
    fastapi_testclient: TestClient,
) -> None:
    request = {
        "event_type": "TEST",
        "payload": {"test": True, "info": "TEST"},
        "occurred_at": 1000000000,
    }

    response = fastapi_testclient.post("/events/", json=request)

    assert response.status_code == 200

    assert response.json()["event_type"] == request["event_type"]

    assert response.json()["payload"] == request["payload"]

    assert response.json()["occurred_at"] == request["occurred_at"]

    assert response.json()["event_id"]


# INVALID CASES


def test_register_event_handler_returns_422_when_request_info_is_missing(
    fastapi_testclient: TestClient,
) -> None:
    request = {}

    response = fastapi_testclient.post("/events/", json=request)

    assert response.status_code == 422


def test_register_event_handler_returns_500_on_internal_error(
    broken_fastapi_testclient_factory: Callable[..., TestClient],
    broken_register_event: BrokenRegisterEventUseCase,
) -> None:
    broken_fastapi_testclient = broken_fastapi_testclient_factory(
        register_event=broken_register_event
    )
    request = {
        "event_type": "USER_CREATED",
        "payload": {"user_id": 123, "email": "user@email.com"},
        "occurred_at": 1700000000,
    }

    response = broken_fastapi_testclient.post("/events/", json=request)

    assert response.status_code == 500

    assert response.json()["detail"]
