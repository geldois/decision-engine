import pytest

from app.domain.decisions.decision_outcome import DecisionOutcome
from app.application.dto.decision_status import DecisionStatus
from app.application.mappers.decision_outcome_to_status_mapper import map_outcome_to_status

# tests
def test_map_outcome_to_status_always_returns_correct_statuses_when_receives_valid_outcomes():
    for member in DecisionOutcome:
        assert map_outcome_to_status(member) is DecisionStatus[member.name]
        