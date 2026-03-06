from typing import List

from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.domain.rules.rule import Rule

class InMemoryRuleRepository(RuleRepositoryContract):
    # initializer
    def __init__(self):
        self._next_id = 1
        self._rules = []

    # methods

    # interface methods
    def save(
        self, 
        rule: Rule
    ) -> Rule:
        if rule.rule_id is None:
            rule.rule_id = self._next_id
            self._next_id += 1
            self._rules.append(rule)
        
        return rule
    
    def delete(
        self, 
        rule: Rule
    ) -> bool:
        if rule in self._rules:
            self._rules.remove(rule)
            
            return True
        
        return False
    
    def get_by_id(
        self, 
        rule_id: int
    ) -> Rule | None:
        for r in self._rules:
            if r.rule_id == rule_id:
                return r
        
        return None

    def list_all(self) -> List[Rule]:
        return self._rules
    