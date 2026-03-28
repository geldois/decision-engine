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
from app.domain.exceptions.event_exception import EventException
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
# invalid cases
# ==========
def test_register_event_handler_returns_422_when_request_info_is_missing(
    client: TestClient,
):
    request_payload = {}

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 422


class BrokenRegisterEventUseCase(RegisterEventUseCase):
    def execute(self, dto_request: RegisterEventDtoRequest) -> RegisterEventDtoResponse:
        raise RuntimeError("boom")


def test_register_event_handler_returns_500_on_internal_error(client: TestClient):
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


# ----------
# domain exceptions
# ----------
def test_register_event_handler_returns_422_when_event_payload_is_empty(
    client: TestClient,
):
    request_payload = {
        "event_type": "USER_CREATED",
        "payload": {},
        "timestamp": 1700000000,
    }
    event_exception = EventException.event_payload_cannot_be_empty()

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 422

    assert response_payload.json()["detail"]["error"] == event_exception.exception_code

    assert response_payload.json()["detail"]["message"] == event_exception.message


def test_register_event_handler_returns_422_when_timestamp_is_negative(
    client: TestClient,
):
    request_payload = {
        "event_type": "USER_CREATED",
        "payload": {"user_id": 123, "email": "user@email.com"},
        "timestamp": -1,
    }
    event_exception = EventException.event_timestamp_cannot_be_negative()

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 422

    assert response_payload.json()["detail"]["error"] == event_exception.exception_code

    assert response_payload.json()["detail"]["message"] == event_exception.message


def test_register_event_handler_returns_422_when_timestamp_is_zero(
    client: TestClient,
):
    request_payload = {
        "event_type": "USER_CREATED",
        "payload": {"user_id": 123, "email": "user@email.com"},
        "timestamp": 0000000000,
    }
    event_exception = EventException.event_timestamp_cannot_be_zero()

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 422

    assert response_payload.json()["detail"]["error"] == event_exception.exception_code

    assert response_payload.json()["detail"]["message"] == event_exception.message


def test_register_event_handler_returns_422_when_event_type_is_empty(
    client: TestClient,
):
    request_payload = {
        "event_type": " ",
        "payload": {"user_id": 123, "email": "user@email.com"},
        "timestamp": 1700000000,
    }
    event_exception = EventException.event_type_cannot_be_empty()

    response_payload = client.post("/events/", json=request_payload)

    assert response_payload.status_code == 422

    assert response_payload.json()["detail"]["error"] == event_exception.exception_code

    assert response_payload.json()["detail"]["message"] == event_exception.message
