from uuid import UUID

from app.application.contracts.repository import (
    RuleRepository,
)
from app.domain.entities.rule import Rule
from app.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage


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
