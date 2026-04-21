from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.application.dto.dto_register_rule_response import DTORegisterRuleResponse
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.config.container import Container


class BrokenRegisterRuleUseCase(RegisterRuleUseCase):
    def execute(self, dto: DTORegisterRuleRequest) -> DTORegisterRuleResponse:
        raise RuntimeError("boom")


@pytest.fixture(scope="function")
def broken_register_rule(container: Container) -> BrokenRegisterRuleUseCase:
    return BrokenRegisterRuleUseCase(uow_factory=container.db.uow_factory)


# VALID CASES


def test_register_rule_handler_returns_200_and_valid_http_response(
    fastapi_testclient: TestClient,
) -> None:
    request = {
        "name": "ALWAYS_APPLIES",
        "condition": {
            "type": "simple",
            "field": "event_type",
            "operator": "==",
            "value": "USER_CREATED",
        },
        "outcome": "approved",
        "priority": 0,
    }

    response = fastapi_testclient.post("/rules/", json=request)

    assert response.status_code == 200

    assert response.json()["name"] == request["name"]

    assert response.json()["condition"] == request["condition"]

    assert response.json()["outcome"] == request["outcome"]

    assert response.json()["priority"] == request["priority"]

    assert response.json()["rule_id"]


# INVALID CASES


def test_register_rule_handler_returns_422_when_info_is_missing(
    fastapi_testclient: TestClient,
) -> None:
    request = {}

    response = fastapi_testclient.post("/rules/", json=request)

    assert response.status_code == 422


def test_register_rule_handler_returns_500_on_internal_error(
    broken_fastapi_testclient_factory: Callable[..., TestClient],
    broken_register_rule: BrokenRegisterRuleUseCase,
) -> None:
    broken_fastapi_tesclient = broken_fastapi_testclient_factory(
        register_rule=broken_register_rule
    )
    request = {
        "name": "ALWAYS_APPLIES",
        "condition": {
            "type": "simple",
            "field": "event_type",
            "operator": "==",
            "value": "USER_CREATED",
        },
        "outcome": "approved",
        "priority": 0,
    }

    response = broken_fastapi_tesclient.post("/rules/", json=request)

    assert response.status_code == 500

    assert response.json()["detail"]
