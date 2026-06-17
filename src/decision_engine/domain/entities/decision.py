from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.domain.entities.domain_entity import DomainEntity
from decision_engine.domain.errors.decision_error import (
    MatchedRuleWithNoMatchOutcomeError,
    UnmatchedRuleWithoutNoMatchOutcomeError,
)
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID

    from decision_engine.domain.value_objects.decision_trace import DecisionTrace


class Decision(DomainEntity):
    def __init__(  # noqa: PLR0913
        self,
        *,
        event_id: UUID,
        rule_id: UUID | None,
        outcome: DecisionOutcome,
        traces: tuple[DecisionTrace, ...],
        created_at: datetime | None = None,
        decision_id: UUID | None = None,
    ) -> None:
        if rule_id and outcome is DecisionOutcome.NO_MATCH:
            raise MatchedRuleWithNoMatchOutcomeError

        if not rule_id and outcome is not DecisionOutcome.NO_MATCH:
            raise UnmatchedRuleWithoutNoMatchOutcomeError

        self.event_id = event_id
        self.rule_id = rule_id
        self.outcome = outcome
        self.traces = traces
        super().__init__(created_at=created_at, entity_id=decision_id)

    def is_structurally_equal(self, other: DomainEntity) -> bool:
        if not isinstance(other, Decision):
            return False

        return (
            self.event_id == other.event_id
            and self.rule_id == other.rule_id
            and self.outcome == other.outcome
            and self.traces == other.traces
            and self.created_at == other.created_at
        )
