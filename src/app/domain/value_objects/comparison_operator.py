from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from operator import eq, gt, lt, ne
from typing import Any


class ComparisonOperator(Enum):
    _function: Callable[..., bool]

    EQUALS = "==", eq
    GREATER_THAN = ">", gt
    LESS_THAN = "<", lt
    NOT_EQUALS = "!=", ne

    def __new__(
        cls, operator: str, _function: Callable[..., bool]
    ) -> ComparisonOperator:
        obj = object.__new__(cls)
        obj._value_ = operator
        obj._function = _function

        return obj

    def evaluate(self, left: Any, right: Any, /) -> bool:
        return self._function(left, right)
