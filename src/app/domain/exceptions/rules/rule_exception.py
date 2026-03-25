from __future__ import annotations

from app.domain.exceptions.domain_exception import DomainException
from app.domain.value_objects.exponible_event_field import ExponibleEventField
from app.domain.value_objects.rule_operator import RuleOperator


class RuleException(DomainException):
    @classmethod
    def rule_condition_cannot_be_builded(
        cls,
        condition_field: ExponibleEventField,
        condition_operator: RuleOperator,
        condition_value: int | str,
    ) -> RuleException:
        return cls(
            f"Rule condition cannot be builded \
                (field: {condition_field} \
                    | operator: {condition_operator} \
                        | value: {condition_value})"
        )

    @classmethod
    def rule_condition_value_cannot_be_empty(cls) -> RuleException:
        return cls("Rule condition value cannot be empty")

    @classmethod
    def rule_name_cannot_be_empty(cls) -> RuleException:
        return cls("Rule name cannot be empty")
