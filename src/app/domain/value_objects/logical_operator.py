from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from operator import and_, or_


class LogicalOperator(Enum):
    _function: Callable[..., bool]

    AND = "and", and_
    OR = "or", or_

    def __new__(cls, operator: str, _funtion: Callable[..., bool]) -> LogicalOperator:
        obj = object.__new__(cls)
        obj._value_ = operator
        obj._function = _funtion

        return obj

    def evaluate(self, list_of_conditions: list[bool], /) -> bool:
        return self._function(list_of_conditions)
