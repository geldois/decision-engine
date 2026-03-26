from collections.abc import Callable
from operator import eq, gt, lt, ne
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity
from app.domain.entities.event import Event
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.exponible_event_field import ExponibleEventField
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
        condition_field: ExponibleEventField,
        condition_operator: RuleOperator,
        condition_value: int | str,
        outcome: DecisionOutcome,
        rule_id: UUID | None = None,
    ) -> None:

        if not name.strip():
            raise RuleException.rule_name_cannot_be_empty()

        if isinstance(condition_value, str) and not condition_value.strip():
            raise RuleException.rule_condition_value_cannot_be_empty()

        if not condition_value:
            raise RuleException.rule_condition_value_cannot_be_empty()

        self.name = name.strip()
        self.condition_field = condition_field
        self.condition_operator = condition_operator
        self.condition_value = condition_value
        self.outcome = outcome
        super().__init__(rule_id)

    def build_condition(
        self,
        condition_field: ExponibleEventField,
        condition_operator: RuleOperator,
        condition_value: str | int,
    ) -> Callable[[Event], bool]:
        try:

            def condition(event: Event) -> bool:
                operator_function = _MAPPING[condition_operator]

                return operator_function(
                    event.get_field_value(condition_field), condition_value
                )
        except Exception as exception:
            raise RuleException.rule_condition_cannot_be_builded(
                condition_field=condition_field,
                condition_operator=condition_operator,
                condition_value=condition_value,
            ) from exception

        return condition

    def applies_to(self, event: Event) -> bool:
        condition = self.build_condition(
            condition_field=self.condition_field,
            condition_operator=self.condition_operator,
            condition_value=self.condition_value,
        )

        return condition(event)
