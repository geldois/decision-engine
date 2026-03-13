from app.application.mappers.decision_result_mapper import map_outcome_to_result, map_result_to_outcome
from app.application.types.decision_result import DecisionResult
from app.domain.entities.decisions.decision_outcome import DecisionOutcome

# tests
def test_map_outcome_to_result_always_returns_correct_results():
    for member in DecisionOutcome:
        assert map_outcome_to_result(member) is DecisionResult[member.name]
        
def test_map_result_to_outcome_always_returns_correct_outcomes():
    for member in DecisionResult:
        assert map_result_to_outcome(member) is DecisionOutcome(member.value)
