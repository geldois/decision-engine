from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.application.contracts.repository import (
    RuleRepository,
)

if TYPE_CHECKING:
    from uuid import UUID

    from decision_engine.domain.entities.rule import Rule
    from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage


class MemRuleRepository(RuleRepository):
    def __init__(self, storage: MemStorage) -> None:
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
