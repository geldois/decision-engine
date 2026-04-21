from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from app.application.dto.dto_produce_decision_request import DTOProduceDecisionRequest
from app.application.dto.dto_produce_decision_response import DTOProduceDecisionResponse
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.config.container import Container
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule


class BrokenProduceDecisionUseCase(ProduceDecisionUseCase):
    def execute(self, dto: DTOProduceDecisionRequest) -> DTOProduceDecisionResponse:
        raise RuntimeError("boom")


@pytest.fixture(scope="function")
def broken_produce_decision(container: Container) -> BrokenProduceDecisionUseCase:
    return BrokenProduceDecisionUseCase(uow_factory=container.db.uow_factory)


# VALID CASES


def test_produce_decision_handler_returns_200_and_valid_http_response(
    event_factory: Callable[..., Event],
    rule_factory: Callable[..., Rule],
    container: Container,
    fastapi_testclient: TestClient,
) -> None:
    event = event_factory()
    rule = rule_factory()

    with container.db.uow_factory() as uow:
        uow.events.save(event=event)
        uow.rules.save(rule=rule)

    request = {"event_id": str(event.id)}

    response = fastapi_testclient.post("/decisions/", json=request)

    assert response.status_code == 200

    assert response.json()["event_id"] == str(event.id)

    assert response.json()["rule_id"] == str(rule.id)

    assert response.json()["status"] == rule.outcome.value

    assert response.json()["traces"]

    assert response.json()["decision_id"]


# INVALID CASES


def test_produce_decision_handler_returns_422_when_info_is_missing(
    fastapi_testclient: TestClient,
) -> None:
    request = {}

    response = fastapi_testclient.post("/decisions/", json=request)

    assert response.status_code == 422


def test_produce_decision_handler_returns_500_on_internal_error(
    event_factory: Callable[..., Event],
    broken_fastapi_testclient_factory: Callable[..., TestClient],
    broken_produce_decision: BrokenProduceDecisionUseCase,
) -> None:
    event = event_factory()
    broken_fastapi_testclient = broken_fastapi_testclient_factory(
        produce_decision=broken_produce_decision
    )
    request = {"event_id": str(event.id)}

    response = broken_fastapi_testclient.post("/decisions/", json=request)

    assert response.status_code == 500

    assert response.json()["detail"]
