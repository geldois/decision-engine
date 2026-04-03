from datetime import datetime
from uuid import UUID

from app.domain.entities.domain_entity import DomainEntity
from app.domain.exceptions.decision_exception import DecisionException
from app.domain.value_objects.decision_outcome import DecisionOutcome


class Decision(DomainEntity):
    def __init__(
        self,
        event_id: UUID,
        rule_id: UUID | None,
        outcome: DecisionOutcome,
        explanation: str,
        created_at: datetime | None = None,
        decision_id: UUID | None = None,
    ) -> None:
        if rule_id and outcome is DecisionOutcome.NO_MATCH:
            raise DecisionException.decision_with_rule_cannot_be_no_match(
                details={"rule_id": rule_id, "outcome": outcome}
            )

        if not rule_id and outcome is not DecisionOutcome.NO_MATCH:
            raise DecisionException.decision_without_rule_must_be_no_match(
                details={"rule_id": rule_id, "outcome": outcome}
            )

        if not explanation.strip():
            raise DecisionException.decision_explanation_cannot_be_empty(
                details={"explanation": explanation}
            )

        self.event_id = event_id
        self.rule_id = rule_id
        self.outcome = outcome
        self.explanation = explanation
        super().__init__(created_at=created_at, entity_id=decision_id)
