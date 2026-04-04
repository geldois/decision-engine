from app.domain.value_objects.comparison_operator import ComparisonOperator
from app.domain.value_objects.logical_operator import LogicalOperator


class Condition:
    def evaluate(self) -> bool: ...
