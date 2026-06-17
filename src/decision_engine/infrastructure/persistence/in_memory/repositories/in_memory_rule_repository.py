from uuid import UUID

from decision_engine.application.contracts.repository import (
    RuleRepository,
)
from decision_engine.domain.entities.rule import Rule
from decision_engine.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage


class InMemoryRuleRepository(RuleRepository):
    def __init__(self, storage: InMemoryStorage) -> None:
        self.rules = storage.rules

    def save(self, rule: Rule) -> Rule:
        self.rules[rule.id] = rule

        return rule

    def delete(self, rule: Rule) -> bool:
        if rule.id in self.rules:
            self.rules.pop(rule.id)

            return True

        return False

    def get_by_id(self, rule_id: UUID) -> Rule | None:
        return self.rules.get(rule_id, None)

    def list_all(self) -> list[Rule]:
        return list(self.rules.values())
