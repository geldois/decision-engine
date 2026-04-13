from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from app.domain.value_objects.decision_trace import (
        CompositeDecisionTrace,
        SimpleDecisionTrace,
    )

T = TypeVar("T")


class DecisionTraceVisitor[T](ABC):
    @abstractmethod
    def visit_composite(self, element: CompositeDecisionTrace) -> T:
        raise NotImplementedError()

    @abstractmethod
    def visit_simple(self, element: SimpleDecisionTrace) -> T:
        raise NotImplementedError()
