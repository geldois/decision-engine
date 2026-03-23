from uuid import UUID

from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.domain_entity import DomainEntity
from app.domain.exceptions.decisions.decision_exception import DecisionException


class Decision(DomainEntity):
    def __init__(
        self,
        event_id: UUID,
        rule_id: UUID | None,
        outcome: DecisionOutcome,
        explanation: str,
        decision_id: UUID | None = None,
    ) -> None:

        if rule_id and outcome is DecisionOutcome.NO_MATCH:
            raise DecisionException.decision_with_rule_cannot_be_no_match(
                outcome=outcome
            )

        if not rule_id and outcome is not DecisionOutcome.NO_MATCH:
            raise DecisionException.decision_without_rule_must_be_no_match(
                outcome=outcome
            )

        if not explanation.strip():
            raise DecisionException.decision_explanation_cannot_be_empty()

        self.event_id = event_id
        self.rule_id = rule_id
        self.outcome = outcome
        self.explanation = explanation
        super().__init__(decision_id)
