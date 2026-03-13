from app.application.types.decision_result import DecisionResult
from app.domain.entities.decisions.decision_outcome import DecisionOutcome

_MAPPING = {
    DecisionOutcome.APPROVED: DecisionResult.APPROVED, 
    DecisionOutcome.NO_MATCH: DecisionResult.NO_MATCH, 
    DecisionOutcome.REJECTED: DecisionResult.REJECTED
}

# functions
def map_outcome_to_result(outcome: DecisionOutcome) -> DecisionResult:
    return _MAPPING[outcome]

def map_result_to_outcome(status: DecisionResult | str) -> DecisionOutcome:
    if isinstance(status, DecisionResult):
        return DecisionOutcome(status.value)

    return DecisionOutcome(status)
