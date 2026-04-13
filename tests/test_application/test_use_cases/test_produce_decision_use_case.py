from uuid import uuid4

import pytest

from app.application.dto.dto_produce_decision_request import DTOProduceDecisionRequest
from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.bootstrap.bootstrap import bootstrap
from app.domain.exceptions.event_exception import EventException


# ==========
# valid cases
# ==========
def test_produce_decision_use_case_returns_valid_dto_response() -> None:
    container = bootstrap(env="test")
    dto_register_event_request = DTORegisterEventRequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    dto_register_rule_request = DTORegisterRuleRequest(
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
    dto_register_event_response = container.register_event_use_case.execute(
        dto=dto_register_event_request
    )
    dto_register_rule_response = container.register_rule_use_case.execute(
        dto=dto_register_rule_request
    )
    dto_produce_decision_request = DTOProduceDecisionRequest(
        event_id=dto_register_event_response.event_id
    )

    dto_produce_decision_response = container.produce_decision_use_case.execute(
        dto=dto_produce_decision_request
    )

    assert (
        dto_produce_decision_response.event_id == dto_register_event_response.event_id
    )

    assert dto_produce_decision_response.rule_id == dto_register_rule_response.rule_id

    assert dto_produce_decision_response.status == dto_register_rule_response.outcome

    assert dto_produce_decision_response.traces

    assert dto_produce_decision_response.decision_id


# ==========
# invalid cases
# ==========
def test_produce_decision_use_case_raises_on_not_found_event() -> None:
    container = bootstrap(env="test")
    dto_produce_decision_request = DTOProduceDecisionRequest(event_id=uuid4())

    with pytest.raises(EventException):
        container.produce_decision_use_case.execute(dto=dto_produce_decision_request)
