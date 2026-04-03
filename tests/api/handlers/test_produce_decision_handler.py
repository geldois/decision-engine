from fastapi.testclient import TestClient

from app.application.dto.dto_produce_decision_request import DTOProduceDecisionRequest
from app.application.dto.dto_produce_decision_response import DTOProduceDecisionResponse
from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.bootstrap.bootstrap import (
    bootstrap,
    build_in_memory_unit_of_work_factory,
    create_app,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


# ==========
# valid cases
# ==========
def test_produce_decision_handler_returns_200_and_valid_http_response() -> None:
    container = bootstrap(env="test")
    app = create_app(container=container)
    client = TestClient(app, raise_server_exceptions=True)
    dto_register_event_request = DTORegisterEventRequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    dto_register_rule_request = DTORegisterRuleRequest(
        name="ALWAYS_APPLIES",
        condition_field="event_type",
        condition_operator="==",
        condition_value="USER_CREATED",
        outcome="approved",
        priority=0,
    )
    dto_register_event_response = container.register_event_use_case.execute(
        dto_request=dto_register_event_request
    )
    dto_register_rule_response = container.register_rule_use_case.execute(
        dto_request=dto_register_rule_request
    )
    request_payload = {"event_id": str(dto_register_event_response.event_id)}

    response_payload = client.post("/decisions/", json=request_payload)

    assert response_payload.status_code == 200

    assert response_payload.json()["event_id"] == str(
        dto_register_event_response.event_id
    )

    assert response_payload.json()["rule_id"] == str(dto_register_rule_response.rule_id)

    assert response_payload.json()["status"] == dto_register_rule_response.outcome.value

    assert response_payload.json()["explanation"]

    assert response_payload.json()["decision_id"]


# ==========
# invalid cases
# ==========
def test_produce_decision_handler_returns_422_when_info_is_missing() -> None:
    container = bootstrap(env="test")
    app = create_app(container=container)
    client = TestClient(app, raise_server_exceptions=True)
    request_payload = {}

    response_payload = client.post("/decisions/", json=request_payload)

    assert response_payload.status_code == 422


class BrokenProduceDecisionUseCase(ProduceDecisionUseCase):
    def execute(
        self, dto_request: DTOProduceDecisionRequest
    ) -> DTOProduceDecisionResponse:
        raise RuntimeError("boom")


def test_produce_decision_handler_returns_500_on_internal_error() -> None:
    unit_of_work_factory = build_in_memory_unit_of_work_factory(
        in_memory_storage=InMemoryStorage()
    )
    overrides = {
        "produce_decision_use_case": BrokenProduceDecisionUseCase(
            unit_of_work_factory=unit_of_work_factory
        )
    }
    container = bootstrap(env="test", overrides=overrides)
    app = create_app(container=container)
    client = TestClient(app, raise_server_exceptions=True)
    dto_register_event_request = DTORegisterEventRequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    dto_register_event_response = container.register_event_use_case.execute(
        dto_request=dto_register_event_request
    )
    request_payload = {"event_id": str(dto_register_event_response.event_id)}

    response_payload = client.post("/decisions/", json=request_payload)

    assert response_payload.status_code == 500

    assert response_payload.json()["detail"]
