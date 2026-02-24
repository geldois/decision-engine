from app.domain.events.event import Event
from app.domain.decisions.decision_outcome import DecisionOutcome

class Rule:
    # initializer
    def __init__(
        self, 
        name: str, 
        condition: callable, 
        outcome: DecisionOutcome, 
        rule_id: int | None = None
    ):
        # invariants
        if name is None or not isinstance(name, str) or not name.strip():
            raise ValueError("Rule name is required.")
        
        if condition is None or not callable(condition):
            raise ValueError("Rule condition is required.")
        
        if outcome is None or not isinstance(outcome, DecisionOutcome):
            raise ValueError("Rule outcome is required.")
        
        if rule_id is not None and (not isinstance(rule_id, int) or rule_id < 0):
            raise ValueError("Rule id is invalid.")
        
        # instance attributes
        self.name = name.strip()
        self.condition = condition
        self.outcome = outcome
        self.rule_id = rule_id

    # methods
    def applies_to(
        self, 
        event: Event
    ) -> bool:
        return self.condition(event)
    