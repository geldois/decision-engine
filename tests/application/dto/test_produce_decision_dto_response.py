from dataclasses import FrozenInstanceError, fields
from uuid import UUID, uuid4

import pytest

from app.application.dto.produce_decision_dto_response import ProduceDecisionDtoResponse
from app.application.types.decision_result import DecisionResult


def test_produce_decision_dto_response_is_immutable():
    produce_decision_dto_response = ProduceDecisionDtoResponse(
        event_id=uuid4(),
        rule_id=None,
        status=DecisionResult.NO_MATCH,
        explanation="No match",
        decision_id=uuid4(),
    )

    assert isinstance(produce_decision_dto_response.event_id, UUID)

    assert isinstance(produce_decision_dto_response.rule_id, UUID | None)

    assert isinstance(produce_decision_dto_response.status, DecisionResult)

    assert isinstance(produce_decision_dto_response.explanation, str)

    assert isinstance(produce_decision_dto_response.decision_id, UUID)

    assert {f.name for f in fields(ProduceDecisionDtoResponse)} == {
        "event_id",
        "rule_id",
        "status",
        "explanation",
        "decision_id",
    }

    with pytest.raises(FrozenInstanceError):
        produce_decision_dto_response.event_id = uuid4()

    with pytest.raises(FrozenInstanceError):
        produce_decision_dto_response.rule_id = uuid4()

    with pytest.raises(FrozenInstanceError):
        produce_decision_dto_response.status = DecisionResult.NO_MATCH

    with pytest.raises(FrozenInstanceError):
        produce_decision_dto_response.explanation = "No match"

    with pytest.raises(FrozenInstanceError):
        produce_decision_dto_response.decision_id = uuid4()
