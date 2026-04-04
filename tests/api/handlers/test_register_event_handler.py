import pytest
from fastapi.testclient import TestClient

from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.application.dto.dto_register_event_response import DTORegisterEventResponse
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.bootstrap.bootstrap import (
    bootstrap,
    build_in_memory_unit_of_work_factory,
    create_app,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


@pytest.fixture
def client() -> TestClient:
    container = bootstrap(env="test")
    app = create_app(container=container)

    return TestClient(app, raise_server_exceptions=True)


# ==========
# valid cases
# ==========
def test_register_event_handler_returns_200_and_valid_http_response(
    client: TestClient,
) -> None:
    request_payload = {
        "event_type": "USER_CREATED",
        "payload": {"user_id": 123, "email": "user@email.com"},
        "occurred_at": 1700000000,
    }

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 200

    assert response_payload.json()["event_type"] == request_payload["event_type"]

    assert response_payload.json()["payload"] == request_payload["payload"]

    assert response_payload.json()["occurred_at"] == request_payload["occurred_at"]

    assert response_payload.json()["event_id"]


# ==========
# invalid cases
# ==========
def test_register_event_handler_returns_422_when_request_info_is_missing(
    client: TestClient,
) -> None:
    request_payload = {}

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 422


class BrokenRegisterEventUseCase(RegisterEventUseCase):
    def execute(self, dto_request: DTORegisterEventRequest) -> DTORegisterEventResponse:
        raise RuntimeError("boom")


def test_register_event_handler_returns_500_on_internal_error(
    client: TestClient,
) -> None:
    unit_of_work_factory = build_in_memory_unit_of_work_factory(
        in_memory_storage=InMemoryStorage()
    )
    overrides = {
        "register_event_use_case": BrokenRegisterEventUseCase(
            unit_of_work_factory=unit_of_work_factory
        )
    }
    container = bootstrap(env="test", overrides=overrides)
    app = create_app(container=container)
    client = TestClient(app, raise_server_exceptions=True)
    request_payload = {
        "event_type": "USER_CREATED",
        "payload": {"user_id": 123, "email": "user@email.com"},
        "occurred_at": 1700000000,
    }

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 500

    assert response_payload.json()["detail"]
