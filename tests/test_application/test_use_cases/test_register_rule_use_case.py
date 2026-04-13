from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.bootstrap.bootstrap import bootstrap


# ==========
# valid cases
# ==========
def test_register_rule_use_case_returns_valid_dto_response() -> None:
    container = bootstrap(env="test")
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

    dto_register_rule_response = container.register_rule_use_case.execute(
        dto=dto_register_rule_request
    )

    assert dto_register_rule_response.name == dto_register_rule_request.name

    assert dto_register_rule_response.condition == dto_register_rule_request.condition

    assert dto_register_rule_response.outcome == dto_register_rule_request.outcome

    assert dto_register_rule_response.priority == dto_register_rule_request.priority

    assert dto_register_rule_response.rule_id
