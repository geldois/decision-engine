from app.application.dto.decision_status import DecisionStatus
from app.domain.decisions.decision_outcome import DecisionOutcome

_MAPPING = {
    DecisionOutcome.APPROVED: DecisionStatus.APPROVED, 
    DecisionOutcome.NO_MATCH: DecisionStatus.NO_MATCH, 
    DecisionOutcome.REJECTED: DecisionStatus.REJECTED
}

# functions
def map_outcome_to_status(outcome: DecisionOutcome) -> DecisionStatus:
    return _MAPPING[outcome]
