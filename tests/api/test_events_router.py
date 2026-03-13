import pytest
from fastapi.testclient import TestClient

from app.application.dto.register_event_dto_request import RegisterEventDtoRequest
from app.application.dto.register_event_dto_response import RegisterEventDtoResponse
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
# valid
# ==========
def test_events_router_register_event_returns_200_and_valid_http_response(
    client: TestClient,
):
    request_payload = {
        "event_type": "USER_CREATED",
        "payload": {"user_id": 123, "email": "user@email.com"},
        "timestamp": 1700000000,
    }

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 200

    assert response_payload.json()["event_type"] == request_payload["event_type"]

    assert response_payload.json()["payload"] == request_payload["payload"]

    assert response_payload.json()["timestamp"] == request_payload["timestamp"]

    assert response_payload.json()["event_id"]


# ==========
# invalid
# ==========
def test_events_router_register_event_returns_422_when_info_is_missing(
    client: TestClient,
):
    request_payload = {}

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 422


class BrokenRegisterEventUseCase(RegisterEventUseCase):
    def execute(self, dto_request: RegisterEventDtoRequest) -> RegisterEventDtoResponse:
        raise RuntimeError("boom")


def test_events_router_register_event_returns_500_on_internal_error(client: TestClient):
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
        "timestamp": 1700000000,
    }

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 500

    assert response_payload.json()["detail"]
