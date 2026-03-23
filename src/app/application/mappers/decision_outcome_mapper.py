from app.domain.exceptions.decision_exception import DecisionException
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.decision_outcome import DecisionOutcome


def map_outcome_by_name(outcome_name: str) -> DecisionOutcome:
    return DecisionOutcome[outcome_name]


def map_outcome_by_value(outcome_value: str) -> DecisionOutcome:
    if not outcome_value.strip():
        raise RuleException.rule_outcome_cannot_be_empty(
            details={"outcome": outcome_value}
        )

    try:
        return DecisionOutcome(outcome_value)
    except ValueError as exception:
        raise DecisionException.decision_outcome_is_invalid(
            details={"outcome": outcome_value}
        ) from exception
