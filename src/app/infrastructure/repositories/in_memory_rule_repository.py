from typing import List

from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.domain.rules.rule import Rule

class InMemoryRuleRepository(RuleRepositoryContract):
    # initializer
    def __init__(self):
        self._rules = {}

    # methods

    # interface methods
    def save(
        self, 
        rule: Rule
    ) -> Rule:
        self._rules[rule._id] = rule
        
        return rule
    
    def delete(
        self, 
        rule: Rule
    ) -> bool:
        if rule._id in self._rules:
            self._rules.pop(rule._id)
            
            return True
        
        return False
    
    def get_by_id(
        self, 
        rule_id: int
    ) -> Rule | None:
        return self._rules.get(rule_id, None)

    def list_all(self) -> List[Rule]:
        return list(self._rules.values())
    