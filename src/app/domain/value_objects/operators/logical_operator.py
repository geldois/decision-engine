from __future__ import annotations

from collections.abc import Iterable
from enum import Enum


class LogicalOperator(Enum):
    stop_value: bool

    AND = "and", False
    OR = "or", True

    def __new__(cls, operator: str, stop_value: bool) -> LogicalOperator:
        obj = object.__new__(cls)
        obj._value_ = operator
        obj.stop_value = stop_value

        return obj

    def compare(self, conditions: Iterable[bool]) -> bool:
        for condition in conditions:
            if condition is self.stop_value:
                return self.stop_value

        return not self.stop_value
