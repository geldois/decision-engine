from functools import partial
from typing import Callable

from app.application.contracts.unit_of_works.unit_of_work_contract import (
    UnitOfWorkContract,
)
from app.application.contracts.use_cases.use_case_contract import UseCaseContract
from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.dto.produce_decision_dto_response import ProduceDecisionDtoResponse
from app.application.mappers.decision_result_mapper import map_outcome_to_result
from app.domain.services.decision_engine import DecisionEngine


class ProduceDecisionUseCase(UseCaseContract):
    def __init__(
        self,
        unit_of_work_factory: Callable[..., UnitOfWorkContract],
        decision_engine: DecisionEngine,
    ) -> None:
        super().__init__(unit_of_work_factory=unit_of_work_factory)
        self.decision_engine = decision_engine

    def execute(
        self, dto_request: ProduceDecisionDtoRequest
    ) -> ProduceDecisionDtoResponse:
        unit_of_work = self.unit_of_work_factory()

        with unit_of_work:
            event = unit_of_work.event_repository.get_by_id(
                event_id=dto_request.event_id
            )
            rules = unit_of_work.rule_repository.list_all()
            if not event:
                raise ValueError("Event not found in ProduceDecisionUseCase")
            decision = self.decision_engine.decide(event=event, rules=rules)
            saved_decision = unit_of_work.decision_repository.save(decision=decision)

            return ProduceDecisionDtoResponse(
                event_id=saved_decision.event_id,
                rule_id=saved_decision.rule_id,
                status=map_outcome_to_result(saved_decision.outcome),
                explanation=saved_decision.explanation,
                decision_id=saved_decision.id,
            )


produce_decision_use_case_factory = partial(
    ProduceDecisionUseCase, decision_engine=DecisionEngine()
)
