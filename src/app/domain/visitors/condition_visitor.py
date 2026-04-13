from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from app.domain.value_objects.condition import (
        CompositeCondition,
        SimpleCondition,
    )

T = TypeVar("T")


class ConditionVisitor[T](ABC):
    @abstractmethod
    def visit_composite(self, element: CompositeCondition) -> T:
        raise NotImplementedError()

    @abstractmethod
    def visit_simple(self, element: SimpleCondition) -> T:
        raise NotImplementedError()
