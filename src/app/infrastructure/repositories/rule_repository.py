from app.domain.rules.rule import Rule

class RuleRepository:
    # constructor
    def __init__(self):
        self._rules = []
    # methods
    def list_all(self):
        return self._rules
    