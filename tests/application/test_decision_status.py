from app.domain.decisions.decision_outcome import DecisionOutcome
from app.application.dto.decision_status import DecisionStatus

# tests
def test_decision_status_values_are_valid_decision_outcomes():
    assert {member.name for member in DecisionStatus} == {member.name for member in DecisionOutcome}
    