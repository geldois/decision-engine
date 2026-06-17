from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from decision_engine.application.dto.requests.produce_decision import ProduceDecisionDTORequest
from decision_engine.application.dto.responses.produce_decision import ProduceDecisionDTOResponse
from decision_engine.application.use_cases.produce_decision import ProduceDecisionUseCase
from decision_engine.config.container import Container
from decision_engine.domain.entities.event import Event
from decision_engine.domain.entities.rule import Rule


class BrokenProduceDecisionUseCase(ProduceDecisionUseCase):
    def execute(self, dto: ProduceDecisionDTORequest) -> ProduceDecisionDTOResponse:
        raise RuntimeError("boom")


@pytest.fixture(scope="function")
def broken_produce_decision(container: Container) -> BrokenProduceDecisionUseCase:
    return BrokenProduceDecisionUseCase(uow_factory=container.db.uow_factory)


# VALID CASES


def test_produce_decision_handler_returns_200_and_valid_http_response(
    make_event: Callable[..., Event],
    make_rule: Callable[..., Rule],
    container: Container,
    fastapi_testclient: TestClient,
) -> None:
    event = make_event()
    rule = make_rule()

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
    make_event: Callable[..., Event],
    broken_fastapi_testclient_factory: Callable[..., TestClient],
    broken_produce_decision: BrokenProduceDecisionUseCase,
) -> None:
    event = make_event()
    broken_fastapi_testclient = broken_fastapi_testclient_factory(
        produce_decision=broken_produce_decision
    )
    request = {"event_id": str(event.id)}

    response = broken_fastapi_testclient.post("/decisions/", json=request)

    assert response.status_code == 500

    assert response.json()["detail"]
