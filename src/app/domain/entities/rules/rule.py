from enum import Enum
from typing import Callable
from uuid import UUID
import operator

from app.domain.entities.domain_entity import DomainEntity
from app.domain.entities.events.event import Event, EventField
from app.domain.entities.decisions.decision_outcome import DecisionOutcome

class RuleOperator(Enum):
    # enum members
    EQUALS = "=="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    GREATER_THAN = ">"

class Rule(DomainEntity):
    __slots__ = (
        "_id", 
        "condition", 
        "condition_field", 
        "condition_operator", 
        "condition_value", 
        "name", 
        "outcome"
    )

    _MAPPING = {
        RuleOperator.EQUALS: operator.eq, 
        RuleOperator.NOT_EQUALS: operator.ne, 
        RuleOperator.LESS_THAN: operator.lt, 
        RuleOperator.GREATER_THAN: operator.gt
    }

    # initializer
    def __init__(
        self, 
        name: str, 
        condition_field: EventField, 
        condition_operator: RuleOperator, 
        condition_value: int | str, 
        outcome: DecisionOutcome, 
        rule_id: UUID | None = None
    ):
        # invariants
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Rule name is required.")
        
        if not condition_field or not isinstance(condition_field, EventField):
            raise ValueError("Rule condition field is required.")
        
        if not condition_operator or not isinstance(condition_operator, RuleOperator):
            raise ValueError("Rule condition operator is required.")
        
        if not condition_value or not isinstance(condition_value, int | str):
            raise ValueError("Rule condition value is required.")
        
        if not outcome or not isinstance(outcome, DecisionOutcome):
            raise ValueError("Rule outcome is required.")
        
        if rule_id and not isinstance(rule_id, UUID):
            raise ValueError("Rule ID is invalid.")
        
        # instance attributes
        self.name = name.strip()
        self.condition_field = condition_field
        self.condition_operator = condition_operator
        self.condition_value = condition_value
        self.condition = self.build_condition(
            condition_field = self.condition_field, 
            condition_operator = self.condition_operator, 
            condition_value = self.condition_value
        )
        self.outcome = outcome
        super().__init__(rule_id)

    # methods
    def build_condition(
        self, 
        condition_field: EventField, 
        condition_operator: RuleOperator, 
        condition_value: str | int
    ) -> Callable[[Event], bool]:
        def condition(event: Event) -> bool:
            try:
                operator_function = self._MAPPING[condition_operator]
                
                return operator_function(
                    event.get_field_value(condition_field), 
                    condition_value
                )
            except Exception:
                return False
        
        return condition
    
    def applies_to(
        self, 
        event: Event
    ) -> bool:
        return self.condition(event)
    