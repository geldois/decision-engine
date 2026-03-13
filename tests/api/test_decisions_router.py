from fastapi.testclient import TestClient

from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.dto.produce_decision_dto_response import ProduceDecisionDtoResponse
from app.application.dto.register_event_dto_request import RegisterEventDtoRequest
from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
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
# valid
# ==========
def test_decisions_router_produce_decision_returns_200_and_valid_http_response():
    container = bootstrap(env="test")
    app = create_app(container=container)
    client = TestClient(app, raise_server_exceptions=True)
    register_event_dto_request = RegisterEventDtoRequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    register_rule_dto_request = RegisterRuleDtoRequest(
        name="ALWAYS_APPLIES",
        condition_field="event_type",
        condition_operator="==",
        condition_value="USER_CREATED",
        outcome="approved",
    )
    register_event_dto_response = container.register_event_use_case.execute(
        dto_request=register_event_dto_request
    )
    register_rule_dto_response = container.register_rule_use_case.execute(
        dto_request=register_rule_dto_request
    )
    request_payload = {"event_id": str(register_event_dto_response.event_id)}

    response_payload = client.post("/decisions/", json=request_payload)

    assert response_payload.status_code == 200

    assert response_payload.json()["event_id"] == str(register_event_dto_response.event_id)

    assert response_payload.json()["rule_id"] == str(register_rule_dto_response.rule_id)

    assert response_payload.json()["status"] == register_rule_dto_response.outcome.value

    assert response_payload.json()["explanation"]

    assert response_payload.json()["decision_id"]


# ==========
# invalid
# ==========
def test_decisions_router_produce_decision_returns_422_when_info_is_missing():
    container = bootstrap(env="test")
    app = create_app(container=container)
    client = TestClient(app, raise_server_exceptions=True)
    request_payload = {}

    response_payload = client.post("/decisions/", json=request_payload)

    assert response_payload.status_code == 422


class BrokenProduceDecisionUseCase(ProduceDecisionUseCase):
    def produce_decision(
        self, dto_request: ProduceDecisionDtoRequest
    ) -> ProduceDecisionDtoResponse:
        raise RuntimeError("boom")


def test_decisions_router_produce_decision_returns_500_on_internal_error():
    unit_of_work_factory = build_in_memory_unit_of_work_factory(
        in_memory_storage=InMemoryStorage()
    )
    overrides = {
        "produce_decision_use_case": ProduceDecisionUseCase(
            unit_of_work_factory=unit_of_work_factory
        )
    }
    container = bootstrap(env="test", overrides=overrides)
    app = create_app(container=container)
    client = TestClient(app, raise_server_exceptions=True)
    register_event_dto_request = RegisterEventDtoRequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
    )
    register_event_dto_response = container.register_event_use_case.execute(
        dto_request=register_event_dto_request
    )
    request_payload = {"event_id": str(register_event_dto_response.event_id)}

    response_payload = client.post("/decisions/", json=request_payload)

    assert response_payload.status_code == 500

    assert response_payload.json()["detail"]
