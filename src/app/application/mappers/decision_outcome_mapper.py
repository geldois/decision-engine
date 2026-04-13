from app.domain.exceptions.decision_exception import DecisionException
from app.domain.exceptions.rule_exception import RuleException
from app.domain.value_objects.decision_outcome import DecisionOutcome


def parse_decision_outcome(value: str) -> DecisionOutcome:
    if not value.strip():
        raise RuleException.rule_outcome_cannot_be_empty(details={"outcome": value})

    try:
        return DecisionOutcome(value)
    except ValueError as exception:
        raise DecisionException.decision_outcome_is_invalid(
            details={"outcome": value}
        ) from exception
