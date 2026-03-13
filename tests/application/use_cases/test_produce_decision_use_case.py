from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.dto.register_event_dto_request import RegisterEventDtoRequest
from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.bootstrap.bootstrap import bootstrap


# ==========
# valid
# ==========
def test_produce_decision_use_case_returns_valid_dto_response():
    container = bootstrap(env="test")
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
    produce_decision_dto_request = ProduceDecisionDtoRequest(
        event_id=register_event_dto_response.event_id
    )

    produce_decision_dto_response = container.produce_decision_use_case.execute(
        dto_request=produce_decision_dto_request
    )

    assert (
        produce_decision_dto_response.event_id == register_event_dto_response.event_id
    )

    assert produce_decision_dto_response.rule_id == register_rule_dto_response.rule_id

    assert (
        produce_decision_dto_response.status.value
        == register_rule_dto_response.outcome.value
    )

    assert produce_decision_dto_response.explanation

    assert produce_decision_dto_response.decision_id
