from app.domain.events.event import Event

class Rule:
    # constructor
    def __init__(self, name: str, condition: callable, outcome: str, rule_id: int = None):
        # validations
        if name is None or not isinstance(name, str) or not name.strip():
            raise ValueError("Rule name is required.")
        if condition is None or not callable(condition):
            raise ValueError("Rule condition is required.")
        if outcome is None or not isinstance(outcome, str) or not outcome.strip():
            raise ValueError("Rule outcome is required.")
        if rule_id is not None and (not isinstance(rule_id, int) or rule_id < 0):
            raise ValueError("Rule id is invalid.")
        # assignments
        self.name = name.strip()
        self.condition = condition
        self.outcome = outcome.strip()
        self.rule_id = rule_id
    # methods
    def applies_to(self, event: Event):
        return self.condition(event)
    