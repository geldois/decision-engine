from __future__ import annotations

from collections.abc import Iterable
from enum import Enum
from typing import Any


class LogicalOperator(Enum):
    stop_value: bool
    accepted_types: tuple[type[Any], ...]

    AND = "and", False, (bool,)
    OR = "or", True, (bool,)

    def __new__(
        cls, operator: str, stop_value: bool, accepted_types: tuple[type[Any], ...]
    ) -> LogicalOperator:
        obj = object.__new__(cls)
        obj._value_ = operator
        obj.stop_value = stop_value
        obj.accepted_types = accepted_types

        return obj

    def evaluate(self, conditions: Iterable[bool]) -> bool:
        for condition in conditions:
            if condition is self.stop_value:
                return self.stop_value

        return not self.stop_value
