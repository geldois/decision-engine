from datetime import datetime
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.conditions.condition import Condition
from app.domain.value_objects.decision_outcome import DecisionOutcome


class Rule(DomainEntity):
    def __init__(
        self,
        name: str,
        condition: Condition,
        outcome: DecisionOutcome,
        priority: int,
        created_at: datetime | None = None,
        rule_id: UUID | None = None,
    ) -> None:
        if not name.strip():
            raise RuleException.rule_name_cannot_be_empty(details={"name": name})

        if priority < 0:
            raise RuleException.rule_priority_is_invalid(details={"priority": priority})

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
