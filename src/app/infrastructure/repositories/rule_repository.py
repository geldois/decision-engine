from app.domain.rules.rule import Rule

class RuleRepository:
    # constructor
    def __init__(self):
        self._next_id = 1
        self._rules = []
    # methods
    def save(self, rule: Rule):
        if rule.rule_id is None:
            rule.rule_id = self._next_id
            self._next_id += 1
            self._rules.append(rule)
    def list_all(self):
        return self._rules
    