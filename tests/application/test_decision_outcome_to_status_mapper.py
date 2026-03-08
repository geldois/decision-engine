from app.application.dto.decision_status import DecisionStatus
from app.application.mappers.decision_outcome_to_status_mapper import map_outcome_to_status
from app.domain.entities.decisions.decision_outcome import DecisionOutcome

# tests
def test_map_outcome_to_status_always_returns_correct_statuses_when_receives_valid_outcomes():
    for member in DecisionOutcome:
        assert map_outcome_to_status(member) is DecisionStatus[member.name]
        