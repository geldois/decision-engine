from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator


@dataclass(frozen=True)
class DecisionTrace(ABC):
    result: bool

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def accept(
        self, visitor: type[DecisionTraceVisitor[VisitorReturnType]]
    ) -> VisitorReturnType:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> DecisionTrace:
        raise NotImplementedError()


@dataclass(frozen=True)
class CompositeDecisionTrace(DecisionTrace):
    operator: LogicalOperator
    traces: tuple[DecisionTrace, ...]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CompositeDecisionTrace):
            return False

        return (
            self.result is other.result
            and self.operator is other.operator
            and self.traces == other.traces
        )

    def accept(
        self, visitor: type[DecisionTraceVisitor[VisitorReturnType]]
    ) -> VisitorReturnType:
        return visitor.visit_composite(element=self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DecisionTrace:
        return cls(
            result=data["result"],
            operator=LogicalOperator(data["operator"]),
            traces=tuple(
                DecisionTraceRegistry.get_class(name=trace["type"]).from_dict(
                    data=trace
                )
                for trace in data["traces"]
            ),
        )


@dataclass(frozen=True)
class SimpleDecisionTrace(DecisionTrace):
    operator: ComparisonOperator
    field: EventField
    expected_value: object
    actual_value: object

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SimpleDecisionTrace):
            return False

        return (
            self.result is other.result
            and self.operator is other.operator
            and self.expected_value == other.expected_value
            and self.actual_value == other.actual_value
        )

    def accept(
        self, visitor: type[DecisionTraceVisitor[VisitorReturnType]]
    ) -> VisitorReturnType:
        return visitor.visit_simple(element=self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DecisionTrace:
        return cls(
            result=data["result"],
            operator=ComparisonOperator(data["operator"]),
            field=EventField(data["field"]),
            expected_value=data["expected_value"],
            actual_value=data["actual_value"],
        )


VisitorReturnType = TypeVar("VisitorReturnType", covariant=True)


class DecisionTraceVisitor[VisitorReturnType](ABC):
    @classmethod
    @abstractmethod
    def visit_composite(cls, element: CompositeDecisionTrace) -> VisitorReturnType:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def visit_simple(cls, element: SimpleDecisionTrace) -> VisitorReturnType:
        raise NotImplementedError()


class DecisionTraceRegistry:
    _mapping: dict[str, type[DecisionTrace]] = {}

    @classmethod
    def register(
        cls, name: str
    ) -> Callable[[type[DecisionTrace]], type[DecisionTrace]]:
        def wrapper(wrapped_class: type[DecisionTrace]) -> type[DecisionTrace]:
            cls._mapping[name] = wrapped_class

            return wrapped_class

        return wrapper

    @classmethod
    def get_class(cls, name: str) -> type[DecisionTrace]:
        if name not in cls._mapping:
            raise ValueError(f"Decision trace type '{name}' is invalid")  # tmp

        return cls._mapping[name]


DecisionTraceRegistry.register(name="composite")(CompositeDecisionTrace)
DecisionTraceRegistry.register(name="simple")(SimpleDecisionTrace)
