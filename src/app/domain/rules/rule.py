class Rule:
    # constructor
    def __init__(self, rule_id: int, rule_name: str, rule_condition: callable, rule_outcome: str):
        # validations
        if rule_id is None or not isinstance(rule_id, int) or rule_id < 0:
            raise ValueError("Rule id is required.")
        if rule_name is None or not isinstance(rule_name, str) or not rule_name.strip():
            raise ValueError("Rule name is required.")
        if rule_condition is None or not callable(rule_condition):
            raise ValueError("Rule condition is required.")
        if rule_outcome is None or not isinstance(rule_outcome, str) or not rule_outcome.strip():
            raise ValueError("Rule outcome is required.")
        # atributions
        self.rule_id = rule_id
        self.rule_name = rule_name.strip()
        self.rule_condition = rule_condition
        self.rule_outcome = rule_outcome.strip()
    # methods
    def applies_to(self, event: object):
        return self.rule_condition(event)
    