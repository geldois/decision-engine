from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from decision_engine.application.use_cases.list_decisions import ListDecisionsUseCase

if TYPE_CHECKING:
    from collections.abc import Callable

    from fastapi.testclient import TestClient

    from decision_engine.application.dto.responses.produce_decision import (
        ProduceDecisionDTOResponse,
    )
    from decision_engine.config.container import Container
    from tests.conftest import MakeEvent, MakeRule


class BrokenListDecisionsUseCase(ListDecisionsUseCase):
    def execute(self, dto: None) -> list[ProduceDecisionDTOResponse]:  # noqa: ARG002
        message = "boom"

        raise RuntimeError(message)


@pytest.fixture
def broken_list_decisions(container: Container) -> BrokenListDecisionsUseCase:
    return BrokenListDecisionsUseCase(uow_factory=container.db.uow_factory)


# VALID CASES


def test_list_decisions_handler_returns_200_and_empty_list(
    fastapi_testclient: TestClient,
) -> None:
    response = fastapi_testclient.get("/decisions/")

    assert response.status_code == 200

    assert response.json() == []


def test_list_decisions_handler_returns_200_and_valid_http_response(
    make_event: MakeEvent,
    make_rule: MakeRule,
    container: Container,
    fastapi_testclient: TestClient,
) -> None:

    event = make_event()
    rule = make_rule()

    with container.db.uow_factory() as uow:
        uow.events.save(event=event)
        uow.rules.save(rule=rule)

    fastapi_testclient.post("/decisions/", json={"event_id": str(event.id)})

    response = fastapi_testclient.get("/decisions/")

    assert response.status_code == 200

    assert len(response.json()) == 1

    assert response.json()[0]["event_id"] == str(event.id)

    assert response.json()[0]["decision_id"]


# INVALID CASES


def test_list_decisions_handler_returns_500_on_internal_error(
    broken_fastapi_testclient_factory: Callable[..., TestClient],
    broken_list_decisions: BrokenListDecisionsUseCase,
) -> None:
    broken_fastapi_testclient = broken_fastapi_testclient_factory(
        list_decisions=broken_list_decisions
    )

    response = broken_fastapi_testclient.get("/decisions/")

    assert response.status_code == 500

    assert response.json()["detail"]
