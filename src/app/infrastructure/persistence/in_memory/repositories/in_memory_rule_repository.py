from uuid import UUID

from app.application.contracts.repositories.rule_repository_contract import (
    RuleRepositoryContract,
)
from app.domain.entities.rule import Rule
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


class InMemoryRuleRepository(RuleRepositoryContract):
    def __init__(self, in_memory_storage: InMemoryStorage) -> None:
        self.rules = in_memory_storage.rules

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
