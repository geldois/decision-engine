from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.application.types.decision_result import DecisionResult
from app.bootstrap.bootstrap import bootstrap


# ==========
# valid
# ==========
def test_register_rule_use_case_returns_valid_dto_response():
    container = bootstrap(env="test")
    register_rule_dto_request = RegisterRuleDtoRequest(
        name="ALWAYS_APPLIES",
        condition_field="event_type",
        condition_operator="==",
        condition_value="USER_CREATED",
        outcome="approved",
    )

    register_rule_dto_response = container.register_rule_use_case.execute(
        dto_request=register_rule_dto_request
    )

    assert register_rule_dto_response.rule_id

    assert register_rule_dto_response.name == register_rule_dto_request.name

    assert register_rule_dto_response.outcome is DecisionResult(
        register_rule_dto_request.outcome
    )
