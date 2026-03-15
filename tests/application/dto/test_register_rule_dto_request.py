from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest


def test_register_rule_dto_request_exposes_only_boundary_fields():
    register_rule_dto_request = RegisterRuleDtoRequest(
        name="ALWAYS_APPLIES",
        condition_field="event_type",
        condition_operator="==",
        condition_value="USER_CREATED",
        outcome="approved",
    )

    assert isinstance(register_rule_dto_request.name, str)

    assert isinstance(register_rule_dto_request.condition_field, str)

    assert isinstance(register_rule_dto_request.condition_operator, str)

    assert isinstance(register_rule_dto_request.condition_value, int | str)

    assert isinstance(register_rule_dto_request.outcome, str)

    assert set(register_rule_dto_request.__slots__) == {
        "condition_field",
        "condition_operator",
        "condition_value",
        "name",
        "outcome",
    }
