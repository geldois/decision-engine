from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from app.domain.entities.event import Event
from app.domain.exceptions.condition_exception import ConditionException
from app.domain.value_objects.decision_trace import (
    CompositeDecisionTrace,
    DecisionTrace,
    SimpleDecisionTrace,
)
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator

if TYPE_CHECKING:
    from app.domain.visitors.condition_visitor import ConditionVisitor, T


class Condition(ABC):
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def accept(self, visitor: ConditionVisitor[T]) -> T:
        raise NotImplementedError()

    @abstractmethod
    def _evaluate_result(self, event: Event) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def evaluate(self, event: Event) -> DecisionTrace:
        raise NotImplementedError()


class CompositeCondition(Condition):
    def __init__(
        self, operator: LogicalOperator, conditions: Sequence[Condition]
    ) -> None:
        if len(conditions) < 2:
            raise ConditionException.condition_is_invalid(details={"condition": self})

        self.operator = operator
        self.conditions = conditions

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CompositeCondition):
            return False

        return self.operator is other.operator and self.conditions == self.conditions

    def accept(self, visitor: ConditionVisitor[T]) -> T:
        return visitor.visit_composite(element=self)

    def _evaluate_result(self, event: Event) -> bool:
        return self.operator.evaluate(
            conditions=(
                condition._evaluate_result(event=event) for condition in self.conditions
            )
        )

    def evaluate(self, event: Event) -> CompositeDecisionTrace:
        return CompositeDecisionTrace(
            result=self._evaluate_result(event=event),
            operator=self.operator,
            traces=tuple(
                condition.evaluate(event=event) for condition in self.conditions
            ),
        )


class SimpleCondition(Condition):
    def __init__(
        self,
        operator: ComparisonOperator,
        field: EventField,
        value: Any,
    ) -> None:
        if not field.validate(value=value):
            raise ConditionException.condition_is_invalid(
                details={"field": field, "operator": operator, "value": value}
            )

        self.operator = operator
        self.field = field
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimpleCondition):
            return False

        return (
            self.operator is other.operator
            and self.field is other.field
            and self.value == other.value
        )

    def accept(self, visitor: ConditionVisitor[T]) -> T:
        return visitor.visit_simple(element=self)

    def _evaluate_result(self, event: Event) -> bool:
        field_value = self.field.get_field_value(event=event)

        if not self.operator.validate(field=field_value, value=self.value):
            raise ConditionException.condition_is_invalid(
                details={
                    "field": self.field,
                    "operator": self.operator,
                    "value": self.value,
                }
            )

        return self.operator.evaluate(
            left=field_value,
            right=self.value,
        )

    def evaluate(self, event: Event) -> SimpleDecisionTrace:
        return SimpleDecisionTrace(
            result=self._evaluate_result(event=event),
            operator=self.operator,
            field=self.field,
            expected_value=self.value,
            actual_value=self.field.get_field_value(event=event),
        )
