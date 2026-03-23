from collections.abc import Callable
from operator import eq, gt, lt, ne
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity
from app.domain.entities.event import Event
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.rule_operator import RuleOperator

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
        condition_field: EventField,
        condition_operator: RuleOperator,
        condition_value: int | str,
        outcome: DecisionOutcome,
        rule_id: UUID | None = None,
    ) -> None:

        if not name.strip():
            raise RuleException.rule_name_cannot_be_empty(details={"name": name})

        # ..........
        # tmp
        # ..........
        """
        if isinstance(condition_field, int) and not isinstance(condition_value, int):
            raise RuleException.rule_condition_cannot_be_built(
                details={
                    "condition_field": condition_field,
                    "condition_operator": condition_operator,
                    "condition_value": condition_value,
                }
            )

        if isinstance(condition_field.value, str) and (
            condition_operator
            not in (
                RuleOperator.EQUALS,
                RuleOperator.NOT_EQUALS,
            )
            or not isinstance(condition_value, str)
        ):
            raise RuleException.rule_condition_cannot_be_built(
                details={
                    "condition_field": condition_field,
                    "condition_operator": condition_operator,
                    "condition_value": condition_value,
                }
            )
        """
        # ..........

        if isinstance(condition_value, str) and not condition_value.strip():
            raise RuleException.rule_condition_value_cannot_be_empty(
                details={
                    "condition_value": condition_value,
                }
            )

        self.name = name
        self.condition_field = condition_field
        self.condition_operator = condition_operator
        self.condition_value = condition_value
        self.outcome = outcome
        super().__init__(rule_id)

    def build_condition(
        self,
        condition_field: EventField,
        condition_operator: RuleOperator,
        condition_value: int | str,
    ) -> Callable[[Event], bool]:
        def condition(event: Event) -> bool:
            operator_function = _MAPPING[condition_operator]

            return operator_function(
                event.get_field_value(condition_field), condition_value
            )

        return condition

    def applies_to(self, event: Event) -> bool:
        condition = self.build_condition(
            condition_field=self.condition_field,
            condition_operator=self.condition_operator,
            condition_value=self.condition_value,
        )

        return condition(event)
