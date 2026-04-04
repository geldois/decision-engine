from __future__ import annotations

import operator
from collections.abc import Callable
from enum import Enum
from numbers import Number
from typing import Any
from uuid import UUID


class ComparisonOperator(Enum):
    _function: Callable[[Any, Any], bool]
    accepted_types: tuple[type[Any], ...]

    EQUALS = "==", operator.eq, (dict, Number, str, UUID)
    GREATER_THAN = ">", operator.gt, (Number,)
    LESS_THAN = "<", operator.lt, (Number,)
    NOT_EQUALS = "!=", operator.ne, (dict, Number, str, UUID)

    def __new__(
        cls,
        operator: str,
        _function: Callable[[Any, Any], bool],
        accepted_types: tuple[type[Any], ...],
    ) -> ComparisonOperator:
        obj = object.__new__(cls)
        obj._value_ = operator
        obj._function = _function
        obj.accepted_types = accepted_types

        return obj

    def _is_number(self, obj: Any) -> bool:
        return isinstance(obj, Number) and not isinstance(obj, bool)

    def _is_valid_type(self, obj: Any) -> bool:
        return isinstance(obj, self.accepted_types)

    def validate(self, field: Any, value: Any) -> bool:
        if not self._is_valid_type(obj=field) or not self._is_valid_type(obj=value):
            return False

        if self._is_number(obj=field) and self._is_number(obj=value):
            return True

        if isinstance(field, dict) and isinstance(value, dict):
            return self in {ComparisonOperator.EQUALS, ComparisonOperator.NOT_EQUALS}
        
        if isinstance(field, str) and isinstance(value, str):
            return self in {ComparisonOperator.EQUALS, ComparisonOperator.NOT_EQUALS}

        if isinstance(field, UUID) and isinstance(value, UUID):
            return self in {ComparisonOperator.EQUALS, ComparisonOperator.NOT_EQUALS}

        return False

    def accepts_type(self, typ: type[Any]) -> bool:
        return typ in self.accepted_types

    def evaluate(self, left: Any, right: Any) -> bool:
        return self._function(left, right)
