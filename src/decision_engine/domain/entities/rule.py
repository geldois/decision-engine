from __future__ import annotations

from datetime import datetime
from uuid import UUID

from decision_engine.domain.entities.domain_entity import DomainEntity
from decision_engine.domain.errors.rule_error import (
    EmptyRuleNameError,
    InvalidRulePriorityError,
)
from decision_engine.domain.value_objects.condition import Condition
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome


class Rule(DomainEntity):
    def __init__(
        self,
        *,
        name: str,
        condition: Condition,
        outcome: DecisionOutcome,
        priority: int,
        created_at: datetime | None = None,
        rule_id: UUID | None = None,
    ) -> None:
        if not name.strip():
            raise EmptyRuleNameError

        if priority < 0:
            raise InvalidRulePriorityError(priority=priority)

        self.name = name
        self.condition = condition
        self.outcome = outcome
        self.priority = priority
        super().__init__(created_at=created_at, entity_id=rule_id)

    def is_structurally_equal(self, other: DomainEntity) -> bool:
        if not isinstance(other, Rule):
            return False

        return (
            self.name == other.name
            and self.condition == other.condition
            and self.outcome == other.outcome
            and self.priority == other.priority
            and self.created_at == other.created_at
        )
