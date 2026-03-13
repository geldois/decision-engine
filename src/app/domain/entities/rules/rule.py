from collections.abc import Callable
from enum import Enum
from operator import eq, gt, lt, ne
from uuid import UUID

from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.domain_entity import DomainEntity
from app.domain.entities.events.event import Event, ExposibleEventField


class RuleOperator(Enum):
    EQUALS = "=="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    GREATER_THAN = ">"


_MAPPING = {
    RuleOperator.EQUALS: eq,
    RuleOperator.NOT_EQUALS: ne,
    RuleOperator.LESS_THAN: lt,
    RuleOperator.GREATER_THAN: gt,
}


class Rule(DomainEntity):
    def __init__(
        self,
        name: str,
        condition_field: ExposibleEventField,
        condition_operator: RuleOperator,
        condition_value: int | str,
        outcome: DecisionOutcome,
        rule_id: UUID | None = None,
    ) -> None:

        if not name.strip():
            raise ValueError("invalid rule name")

        if isinstance(condition_value, str) and not condition_value.strip():
            raise ValueError("invalid condition value")

        if not condition_value:
            raise ValueError("invalid condition value")

        self.name = name.strip()
        self.condition_field = condition_field
        self.condition_operator = condition_operator
        self.condition_value = condition_value
        self.outcome = outcome
        super().__init__(rule_id)

    def build_condition(
        self,
        condition_field: ExposibleEventField,
        condition_operator: RuleOperator,
        condition_value: str | int,
    ) -> Callable[[Event], bool]:
        def condition(event: Event) -> bool:
            try:
                operator_function = _MAPPING[condition_operator]

                return operator_function(
                    event.get_field_value(condition_field), condition_value
                )
            except Exception:
                return False

        return condition

    def applies_to(self, event: Event) -> bool:
        condition = self.build_condition(
            condition_field=self.condition_field,
            condition_operator=self.condition_operator,
            condition_value=self.condition_value,
        )

        return condition(event)
