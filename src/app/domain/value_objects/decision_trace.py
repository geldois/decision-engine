from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.domain.value_objects.operators.logical_operator import LogicalOperator

if TYPE_CHECKING:
    from app.domain.visitors.decision_trace_visitor import DecisionTraceVisitor, T


@dataclass(frozen=True)
class DecisionTrace(ABC):
    result: bool

    @abstractmethod
    def accept(self, visitor: DecisionTraceVisitor[T]) -> T:
        raise NotImplementedError()


@dataclass(frozen=True)
class CompositeDecisionTrace(DecisionTrace):
    operator: LogicalOperator
    traces: tuple[DecisionTrace, ...]

    def accept(self, visitor: DecisionTraceVisitor[T]) -> T:
        return visitor.visit_composite(element=self)


@dataclass(frozen=True)
class SimpleDecisionTrace(DecisionTrace):
    operator: ComparisonOperator
    field: EventField
    expected_value: object
    actual_value: object

    def accept(self, visitor: DecisionTraceVisitor[T]) -> T:
        return visitor.visit_simple(element=self)
