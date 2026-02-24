from app.domain.decisions.decision_outcome import DecisionOutcome
from app.application.dto.decision_status import DecisionStatus

_MAPPING = {
    DecisionOutcome.APPROVED: DecisionStatus.APPROVED, 
    DecisionOutcome.NO_MATCH: DecisionStatus.NO_MATCH, 
    DecisionOutcome.REJECTED: DecisionStatus.REJECTED
}

def map_outcome_to_status(outcome: DecisionOutcome) -> DecisionStatus:
    return _MAPPING[outcome]
