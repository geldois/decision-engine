from app.application.types.decision_result import DecisionResult
from app.domain.entities.decisions.decision_outcome import DecisionOutcome


def test_decision_result_values_are_valid_decision_outcomes():
    assert {member.name for member in DecisionResult} == {
        member.name for member in DecisionOutcome
    }
