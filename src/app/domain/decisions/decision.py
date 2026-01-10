class Decision:
    # constructor
    def __init__(self, event_id: int, rule_id: int, outcome: str, explanation: str, decision_id: int = None):
        # validations
        if event_id is None or not isinstance(event_id, int):
            raise ValueError("Event id is required.")
        if rule_id is not None and not isinstance(rule_id, int):
            raise ValueError("Rule id is required.")
        if outcome is None or not outcome.strip():
            raise ValueError("Rule outcome is required.")
        if explanation is None or not isinstance(explanation, str) or not explanation.strip():
            raise ValueError("Decision explanation is required.")
        if decision_id is not None and (not isinstance(decision_id, int) or decision_id < 0):
            raise ValueError("Decision id is invalid.")
        # atributions
        self.event_id = event_id
        self.rule_id = rule_id
        self.outcome = outcome
        self.explanation = explanation.strip()
        self.decision_id = decision_id
    