from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

import app.infrastructure.persistence.sql.mappers.sql_decision_mapper as SQLDecisionMapper
from app.application.contracts.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.domain.entities.decision import Decision
from app.infrastructure.database.models.decision_model import DecisionModel


class SQLDecisionRepository(DecisionRepositoryContract):
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, decision: Decision) -> Decision:
        decision_model = SQLDecisionMapper.domain_to_model(decision=decision)
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
            return SQLDecisionMapper.model_to_domain(decision_model=decision_model)

        return None

    def list_all(self) -> list[Decision]:
        decision_models = self.session.query(DecisionModel).all()
        decisions: list[Decision] = []

        for decision_model in decision_models:
            decision = SQLDecisionMapper.model_to_domain(decision_model=decision_model)
            decisions.append(decision)

        return decisions
