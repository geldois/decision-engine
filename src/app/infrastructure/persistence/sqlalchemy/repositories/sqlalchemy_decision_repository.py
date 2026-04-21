from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.contracts.repository import DecisionRepository
from app.domain.entities.decision import Decision
from app.infrastructure.persistence.sqlalchemy.mappers.sqlalchemy_decision_mapper import (
    domain_to_model,
    model_to_domain,
)
from app.infrastructure.persistence.sqlalchemy.models.decision_model import (
    DecisionModel,
)


class SQLAlchemyDecisionRepository(DecisionRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, decision: Decision) -> Decision:
        decision_model = domain_to_model(decision=decision)
        self.session.add(decision_model)
        self.session.flush()
        self.session.refresh(decision_model)

        return decision

    def delete(self, decision: Decision) -> bool:
        decision_model = (
            self.session.execute(
                select(DecisionModel).where(DecisionModel.id == decision.id)
            )
            .scalars()
            .first()
        )

        if decision_model:
            self.session.delete(decision_model)
            self.session.flush()

            return True

        return False

    def get_by_id(self, decision_id: UUID) -> Decision | None:
        decision_model = (
            self.session.execute(
                select(DecisionModel).where(DecisionModel.id == decision_id)
            )
            .scalars()
            .first()
        )

        if decision_model:
            return model_to_domain(decision_model=decision_model)

        return None

    def list_all(self) -> list[Decision]:
        decision_models = self.session.query(DecisionModel).all()
        decisions: list[Decision] = []

        for decision_model in decision_models:
            decision = model_to_domain(decision_model=decision_model)
            decisions.append(decision)

        return decisions
