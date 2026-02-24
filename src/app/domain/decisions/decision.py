from app.domain.events.event import Event
from app.domain.rules.rule import Rule
from app.domain.decisions.decision_outcome import DecisionOutcome

class Decision:
    # initializer
    def __init__(
        self, 
        event: Event, 
        rule: Rule | None, 
        outcome: DecisionOutcome, 
        explanation: str, 
        decision_id: int | None = None
    ):
        # invariants
        if event is None or not isinstance(event, Event):
            raise ValueError("Event is required.")
        
        if rule is not None and not isinstance(rule, Rule):
            raise ValueError("Rule is invalid.")
        
        if outcome is None or not isinstance(outcome, DecisionOutcome):
            raise ValueError("Rule outcome is required.")
        
        if rule is None and outcome is not DecisionOutcome.NO_MATCH:
            raise ValueError("The Rule and outcome states are invalid.")
        
        if explanation is None or not isinstance(explanation, str) or not explanation.strip():
            raise ValueError("Decision explanation is required.")
        
        if decision_id is not None and (not isinstance(decision_id, int) or decision_id < 0):
            raise ValueError("Decision id is invalid.")
        
        # instance attributes
        self.event = event
        self.rule = rule
        self.outcome = outcome
        self.explanation = explanation.strip()
        self.decision_id = decision_id
    