from uuid import uuid4

import pytest

from decision_engine.application.dto.requests.produce_decision import ProduceDecisionDTORequest
from decision_engine.application.dto.requests.register_event import RegisterEventDTORequest
from decision_engine.application.dto.requests.register_rule import RegisterRuleDTORequest
from decision_engine.config.container import Container
from decision_engine.domain.errors.event_error import EventError

# VALID CASES


def test_produce_decision_use_case_returns_valid_dto_response(
    container: Container,
) -> None:
    dto_register_event_request = RegisterEventDTORequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    dto_register_rule_request = RegisterRuleDTORequest(
        name="ALWAYS_APPLIES",
        condition={
            "type": "simple",
            "field": "event_type",
            "operator": "==",
            "value": "USER_CREATED",
        },
        outcome="approved",
        priority=0,
    )
    dto_register_event_response = container.use_cases.register_event.execute(
        dto=dto_register_event_request
    )
    dto_register_rule_response = container.use_cases.register_rule.execute(
        dto=dto_register_rule_request
    )
    dto_produce_decision_request = ProduceDecisionDTORequest(
        event_id=dto_register_event_response.event_id
    )

    dto_produce_decision_response = container.use_cases.produce_decision.execute(
        dto=dto_produce_decision_request
    )

    assert (
        dto_produce_decision_response.event_id == dto_register_event_response.event_id
    )

    assert dto_produce_decision_response.rule_id == dto_register_rule_response.rule_id

    assert dto_produce_decision_response.status == dto_register_rule_response.outcome

    assert dto_produce_decision_response.traces

    assert dto_produce_decision_response.decision_id


# INVALID CASES


def test_produce_decision_use_case_raises_on_not_found_event(
    container: Container,
) -> None:
    dto_produce_decision_request = ProduceDecisionDTORequest(event_id=uuid4())

    with pytest.raises(EventError):
        container.use_cases.produce_decision.execute(dto=dto_produce_decision_request)
