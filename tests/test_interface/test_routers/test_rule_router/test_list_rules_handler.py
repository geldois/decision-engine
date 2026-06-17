from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from decision_engine.application.use_cases.list_rules import ListRulesUseCase

if TYPE_CHECKING:
    from collections.abc import Callable

    from fastapi.testclient import TestClient

    from decision_engine.application.dto.responses.register_rule import (
        RegisterRuleDTOResponse,
    )
    from decision_engine.config.container import Container


class BrokenListRulesUseCase(ListRulesUseCase):
    def execute(self, dto: None) -> list[RegisterRuleDTOResponse]:  # noqa: ARG002
        message = "boom"

        raise RuntimeError(message)


@pytest.fixture
def broken_list_rules(container: Container) -> BrokenListRulesUseCase:
    return BrokenListRulesUseCase(uow_factory=container.db.uow_factory)


# VALID CASES


def test_list_rules_handler_returns_200_and_empty_list(
    fastapi_testclient: TestClient,
) -> None:
    response = fastapi_testclient.get("/rules/")

    assert response.status_code == 200

    assert response.json() == []


def test_list_rules_handler_returns_200_and_valid_http_response(
    container: Container,  # noqa: ARG001
    fastapi_testclient: TestClient,
) -> None:
    rule_request = {
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

    fastapi_testclient.post("/rules/", json=rule_request)

    response = fastapi_testclient.get("/rules/")

    assert response.status_code == 200

    assert len(response.json()) == 1

    assert response.json()[0]["name"] == rule_request["name"]

    assert response.json()[0]["rule_id"]


# INVALID CASES


def test_list_rules_handler_returns_500_on_internal_error(
    broken_fastapi_testclient_factory: Callable[..., TestClient],
    broken_list_rules: BrokenListRulesUseCase,
) -> None:
    broken_fastapi_testclient = broken_fastapi_testclient_factory(
        list_rules=broken_list_rules
    )

    response = broken_fastapi_testclient.get("/rules/")

    assert response.status_code == 500

    assert response.json()["detail"]
