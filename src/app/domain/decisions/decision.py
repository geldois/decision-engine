class Decision:
    # constructor
    def __init__(self, decision_id: int, event_id: int, rule_id: int, rule_outcome: str, decision_explanation: str):
        # validations
        if decision_id is None or not isinstance(decision_id, int) or decision_id < 0:
            raise ValueError("Decision id is required.")
        if event_id is None or not isinstance(event_id, int):
            raise ValueError("Event id is required.")
        if rule_id is None or not isinstance(rule_id, int):
            raise ValueError("Rule id is required.")
        if rule_outcome is None or not rule_outcome.strip():
            raise ValueError("Rule outcome is required.")
        if decision_explanation is None or not isinstance(decision_explanation, str) or not decision_explanation.strip():
            raise ValueError("Decision explanation is required.")
        # atributions
        self.decision_id = decision_id
        self.event_id = event_id
        self.rule_id = rule_id
        self.rule_outcome = rule_outcome
        self.decision_explanation = decision_explanation.strip()
    