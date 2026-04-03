from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.bootstrap.bootstrap import bootstrap
from app.domain.value_objects.decision_outcome import DecisionOutcome


# ==========
# valid cases
# ==========
def test_register_rule_use_case_returns_valid_dto_response() -> None:
    container = bootstrap(env="test")
    dto_register_rule_request = DTORegisterRuleRequest(
        name="ALWAYS_APPLIES",
        condition_field="event_type",
        condition_operator="==",
        condition_value="USER_CREATED",
        outcome="approved",
        priority=0,
    )

    dto_register_rule_response = container.register_rule_use_case.execute(
        dto_request=dto_register_rule_request
    )

    assert dto_register_rule_response.rule_id

    assert dto_register_rule_response.name == dto_register_rule_request.name

    assert dto_register_rule_response.outcome is DecisionOutcome(
        dto_register_rule_request.outcome
    )

    assert dto_register_rule_response.priority == dto_register_rule_request.priority
