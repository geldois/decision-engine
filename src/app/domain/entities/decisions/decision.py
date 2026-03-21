from uuid import UUID

from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.domain_entity import DomainEntity


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
            raise ValueError("invalid decision outcome")

        if not rule_id and outcome is not DecisionOutcome.NO_MATCH:
            raise ValueError("invalid decision outcome")

        if not explanation.strip():
            raise ValueError("invalid decision explanation")

        self.event_id = event_id
        self.rule_id = rule_id
        self.outcome = outcome
        self.explanation = explanation
        super().__init__(decision_id)
