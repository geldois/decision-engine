from dataclasses import FrozenInstanceError, fields
from uuid import UUID, uuid4

import pytest

from app.application.dto.register_rule_dto_response import RegisterRuleDtoResponse
from app.application.types.decision_result import DecisionResult


def test_register_rule_dto_response_is_immutable():
    register_rule_dto_response = RegisterRuleDtoResponse(
        name="ALWAYS_APPLIES", outcome=DecisionResult.APPROVED, rule_id=uuid4()
    )

    assert isinstance(register_rule_dto_response.name, str)

    assert isinstance(register_rule_dto_response.outcome, DecisionResult)

    assert isinstance(register_rule_dto_response.rule_id, UUID)

    assert {f.name for f in fields(RegisterRuleDtoResponse)} == {
        "name",
        "outcome",
        "rule_id",
    }

    with pytest.raises(FrozenInstanceError):
        register_rule_dto_response.name = "ALWAYS_APPLIES"

    with pytest.raises(FrozenInstanceError):
        register_rule_dto_response.outcome = DecisionResult.APPROVED

    with pytest.raises(FrozenInstanceError):
        register_rule_dto_response.rule_id = uuid4()
