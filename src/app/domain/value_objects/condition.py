from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from typing import Any, TypeVar

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


class Condition(ABC):
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def accept(
        self, visitor: type[ConditionVisitor[VisitorReturnType]]
    ) -> VisitorReturnType:
        raise NotImplementedError()

    @abstractmethod
    def evaluate_result(self, event: Event) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def evaluate(self, event: Event) -> DecisionTrace:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Condition:
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

        return self.operator is other.operator and self.conditions == other.conditions

    def accept(
        self, visitor: type[ConditionVisitor[VisitorReturnType]]
    ) -> VisitorReturnType:
        return visitor.visit_composite(element=self)

    def evaluate_result(self, event: Event) -> bool:
        return self.operator.evaluate(
            conditions=(
                condition.evaluate_result(event=event) for condition in self.conditions
            )
        )

    def evaluate(self, event: Event) -> CompositeDecisionTrace:
        return CompositeDecisionTrace(
            result=self.evaluate_result(event=event),
            operator=self.operator,
            traces=tuple(
                condition.evaluate(event=event) for condition in self.conditions
            ),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Condition:
        return cls(
            operator=LogicalOperator(data["operator"]),
            conditions=[
                ConditionRegistry.get_class(name=condition["type"]).from_dict(
                    data=condition
                )
                for condition in data["conditions"]
            ],
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

    def accept(
        self, visitor: type[ConditionVisitor[VisitorReturnType]]
    ) -> VisitorReturnType:
        return visitor.visit_simple(element=self)

    def evaluate_result(self, event: Event) -> bool:
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
            result=self.evaluate_result(event=event),
            operator=self.operator,
            field=self.field,
            expected_value=self.value,
            actual_value=self.field.get_field_value(event=event),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Condition:
        return cls(
            operator=ComparisonOperator(data["operator"]),
            field=EventField(data["field"]),
            value=data["value"],
        )


VisitorReturnType = TypeVar("VisitorReturnType", covariant=True)


class ConditionVisitor[VisitorReturnType](ABC):
    @classmethod
    @abstractmethod
    def visit_composite(cls, element: CompositeCondition) -> VisitorReturnType:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def visit_simple(cls, element: SimpleCondition) -> VisitorReturnType:
        raise NotImplementedError()


class ConditionRegistry:
    _mapping: dict[str, type[Condition]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[type[Condition]], type[Condition]]:
        def wrapper(subclass: type[Condition]) -> type[Condition]:
            cls._mapping[name] = subclass

            return subclass

        return wrapper

    @classmethod
    def get_class(cls, name: str) -> type[Condition]:
        if name not in cls._mapping:
            raise ConditionException.condition_type_is_invalid(details={"type": name})

        return cls._mapping[name]


ConditionRegistry.register(name="composite")(CompositeCondition)
ConditionRegistry.register(name="simple")(SimpleCondition)
