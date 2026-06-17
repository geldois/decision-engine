from __future__ import annotations

from typing import TYPE_CHECKING, override

from decision_engine.domain.errors.domain_error import DomainError

if TYPE_CHECKING:
    from uuid import UUID


class DecisionError(DomainError, error_code=None): ...


class NotFoundDecisionError(DecisionError, error_code="DECISION_NOT_FOUND"):
    decision_id: UUID

    @override
    def __init__(self, *, decision_id: UUID) -> None:
        super().__init__(decision_id=decision_id)

    @override
    def _build_message(self) -> str:
        return f"Decision '{self.decision_id}' was not found."


class InvalidDecisionOutcomeError(
    DecisionError, error_code="DECISION_OUTCOME_INVALID"
):
    outcome: str

    @override
    def __init__(self, *, outcome: str) -> None:
        super().__init__(outcome=outcome)

    @override
    def _build_message(self) -> str:
        return f"Invalid decision outcome: '{self.outcome}'."


class MatchedRuleWithNoMatchOutcomeError(
    DecisionError, error_code="DECISION_OUTCOME_INVALID"
):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "A decision with a matched rule cannot have a NO_MATCH outcome."


class UnmatchedRuleWithoutNoMatchOutcomeError(
    DecisionError, error_code="DECISION_OUTCOME_INVALID"
):
    @override
    def __init__(self) -> None:
        super().__init__()

    @override
    def _build_message(self) -> str:
        return "A decision without a matched rule must have a NO_MATCH outcome."
