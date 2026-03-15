from uuid import UUID

from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.domain.entities.rules.rule import Rule
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


class InMemoryRuleRepository(RuleRepositoryContract):
    def __init__(self, in_memory_storage: InMemoryStorage):
        self._rules = in_memory_storage._rules

    def save(self, rule: Rule) -> Rule:
        self._rules[rule._id] = rule

        return rule

    def delete(self, rule: Rule) -> bool:
        if rule._id in self._rules:
            self._rules.pop(rule._id)

            return True

        return False

    def get_by_id(self, rule_id: UUID) -> Rule | None:
        return self._rules.get(rule_id, None)

    def list_all(self) -> list[Rule]:
        return list(self._rules.values())
