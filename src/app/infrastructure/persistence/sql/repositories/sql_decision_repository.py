from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.domain.entities.decisions.decision import Decision
from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.infrastructure.database.models import DecisionModel


class SqlDecisionRepository(DecisionRepositoryContract):
    def __init__(self, session: Session):
        self.session = session

    def convert_decision_model_to_decision(
        self, decision_model: DecisionModel
    ) -> Decision:
        decision = Decision(
            event_id=decision_model.event_id,
            rule_id=decision_model.rule_id,
            outcome=DecisionOutcome(decision_model.outcome),
            explanation=decision_model.explanation,
            decision_id=decision_model._id,
        )

        return decision

    def convert_decision_to_decision_model(self, decision: Decision) -> DecisionModel:
        decision_model = DecisionModel(
            _id=decision._id,
            event_id=decision.event_id,
            rule_id=decision.rule_id,
            outcome=decision.outcome.value,
            explanation=decision.explanation,
        )

        return decision_model

    def save(self, decision: Decision) -> Decision:
        decision_model = self.convert_decision_to_decision_model(decision=decision)
        self.session.add(decision_model)
        self.session.flush()
        self.session.refresh(decision_model)

        return decision

    def delete(self, decision: Decision) -> bool:
        decision_model = (
            self.session.execute(
                select(DecisionModel).where(DecisionModel._id == decision._id)
            )
            .scalars()
            .first()
        )

        if decision_model:
            self.session.delete(decision_model)

            return True

        return False

    def get_by_id(self, decision_id: UUID) -> Decision | None:
        decision_model = (
            self.session.execute(
                select(DecisionModel).where(DecisionModel._id == decision_id)
            )
            .scalars()
            .first()
        )

        if decision_model:
            return self.convert_decision_model_to_decision(
                decision_model=decision_model
            )

        return None

    def list_all(self) -> list[Decision]:
        decision_models = self.session.query(DecisionModel).all()
        decisions = []

        for decision_model in decision_models:
            decision = self.convert_decision_model_to_decision(
                decision_model=decision_model
            )
            decisions.append(decision)

        return decisions
