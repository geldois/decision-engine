from uuid import UUID

from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.domain_entity import DomainEntity


class Decision(DomainEntity):
    __slots__ = ("id", "event_id", "explanation", "outcome", "rule_id")

    def __init__(
        self,
        event_id: UUID,
        rule_id: UUID | None,
        outcome: DecisionOutcome,
        explanation: str,
        decision_id: UUID | None = None,
    ):

        if not event_id or not isinstance(event_id, UUID):
            raise ValueError("Event ID is required.")

        if rule_id and not isinstance(rule_id, UUID):
            raise ValueError("Rule ID is invalid.")

        if not rule_id and outcome is not DecisionOutcome.NO_MATCH:
            raise ValueError("The Rule ID and outcome states are invalid.")

        if not outcome or not isinstance(outcome, DecisionOutcome):
            raise ValueError("Rule outcome is required.")

        if (
            not explanation
            or not isinstance(explanation, str)
            or not explanation.strip()
        ):
            raise ValueError("Decision explanation is required.")

        if decision_id and not isinstance(decision_id, UUID):
            raise ValueError("Decision ID is invalid")

        self.event_id = event_id
        self.rule_id = rule_id
        self.outcome = outcome
        self.explanation = explanation.strip()
        super().__init__(decision_id)
