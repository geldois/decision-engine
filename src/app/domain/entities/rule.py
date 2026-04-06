from collections.abc import Callable
from datetime import datetime
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity
from app.domain.entities.event import Event
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator


class Rule(DomainEntity):
    def __init__(
        self,
        name: str,
        condition_field: EventField,
        condition_operator: ComparisonOperator,
        condition_value: int | str,
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
        self.condition_field = condition_field
        self.condition_operator = condition_operator
        self.condition_value = condition_value
        self.outcome = outcome
        self.priority = priority
        super().__init__(created_at=created_at, entity_id=rule_id)

    def build_condition(
        self,
        condition_field: EventField,
        condition_operator: ComparisonOperator,
        condition_value: int | str,
    ) -> Callable[[Event], bool]:
        def condition(event: Event) -> bool:
            return condition_operator.compare(
                event.get_field_value(condition_field), condition_value
            )

        return condition

    def apply(self, event: Event) -> bool:
        condition = self.build_condition(
            condition_field=self.condition_field,
            condition_operator=self.condition_operator,
            condition_value=self.condition_value,
        )

        return condition(event)
