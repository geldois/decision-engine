import pytest
from fastapi.testclient import TestClient

from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.application.dto.register_rule_dto_response import RegisterRuleDtoResponse
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.bootstrap.bootstrap import (
    bootstrap,
    build_in_memory_unit_of_work_factory,
    create_app,
)
from app.domain.exceptions.rule_exception import RuleException
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


@pytest.fixture
def client():
    container = bootstrap(env="test")
    app = create_app(container=container)

    return TestClient(app, raise_server_exceptions=True)


# ==========
# valid cases
# ==========
def test_register_rule_handler_returns_200_and_valid_http_response(
    client: TestClient,
) -> None:
    request_payload = {
        "name": "ALWAYS_APPLIES",
        "condition_field": "event_type",
        "condition_operator": "==",
        "condition_value": "USER_CREATED",
        "outcome": "approved",
    }

    response_payload = client.post("/rules/", json=request_payload)

    assert response_payload.status_code == 200

    assert response_payload.json()["name"] == request_payload["name"]

    assert response_payload.json()["outcome"] == request_payload["outcome"]

    assert "rule_id" in response_payload.json()


# ==========
# invalid cases
# ==========
def test_register_rule_handler_returns_422_when_info_is_missing(
    client: TestClient,
) -> None:
    request_payload = {}

    response_payload = client.post("/rules/", json=request_payload)

    assert response_payload.status_code == 422


class BrokenRegisterRuleUseCase(RegisterRuleUseCase):
    def execute(self, dto_request: RegisterRuleDtoRequest) -> RegisterRuleDtoResponse:
        raise RuntimeError("boom")


def test_register_rule_handler_returns_500_on_internal_error(
    client: TestClient,
) -> None:
    unit_of_work_factory = build_in_memory_unit_of_work_factory(
        in_memory_storage=InMemoryStorage()
    )
    overrides = {
        "register_rule_use_case": BrokenRegisterRuleUseCase(
            unit_of_work_factory=unit_of_work_factory
        )
    }
    container = bootstrap(env="test", overrides=overrides)
    app = create_app(container=container)
    client = TestClient(app, raise_server_exceptions=True)
    request_payload = {
        "name": "ALWAYS_APPLIES",
        "condition_field": "event_type",
        "condition_operator": "==",
        "condition_value": "USER_CREATED",
        "outcome": "approved",
    }

    response_payload = client.post("/rules/", json=request_payload)

    assert response_payload.status_code == 500

    assert response_payload.json()["detail"]


# ----------
# domain exceptions
# ----------
def test_register_rule_handler_returns_422_when_rule_condition_cannot_be_builded(
    client: TestClient,
) -> None:
    request_payload = {
        "name": "ALWAYS_APPLIES",
        "condition_field": " ",
        "condition_operator": "==",
        "condition_value": "USER_CREATED",
        "outcome": "approved",
    }
    rule_exception = RuleException.rule_condition_cannot_be_builded()

    response_payload = client.post("/rules/", json=request_payload)

    assert response_payload.status_code == 422

    assert response_payload.json()["detail"]["error"] == rule_exception.exception_code

    # ..........
    # tmp
    # ..........
    # assert response_payload.json()["detail"]["message"] == rule_exception.message
    # ..........


def test_register_rule_handler_returns_422_when_rule_condition_value_is_empty(
    client: TestClient,
) -> None:
    request_payload = {
        "name": "ALWAYS_APPLIES",
        "condition_field": "event_type",
        "condition_operator": "==",
        "condition_value": " ",
        "outcome": "approved",
    }
    rule_exception = RuleException.rule_condition_value_cannot_be_empty()

    response_payload = client.post("/rules/", json=request_payload)

    assert response_payload.status_code == 422

    assert response_payload.json()["detail"]["error"] == rule_exception.exception_code

    assert response_payload.json()["detail"]["message"] == rule_exception.message


def test_register_rule_handler_returns_422_when_rule_name_is_empty(
    client: TestClient,
) -> None:
    request_payload = {
        "name": " ",
        "condition_field": "event_type",
        "condition_operator": "==",
        "condition_value": "USER_CREATED",
        "outcome": "approved",
    }
    rule_exception = RuleException.rule_name_cannot_be_empty()

    response_payload = client.post("/rules/", json=request_payload)

    assert response_payload.status_code == 422

    assert response_payload.json()["detail"]["error"] == rule_exception.exception_code

    assert response_payload.json()["detail"]["message"] == rule_exception.message
