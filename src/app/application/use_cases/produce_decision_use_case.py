from collections.abc import Callable

from app.application.contracts.unit_of_work_contract import (
    UnitOfWorkContract,
)
from app.application.contracts.use_case_contract import UseCaseContract
from app.application.dto.dto_produce_decision_request import DTOProduceDecisionRequest
from app.application.dto.dto_produce_decision_response import DTOProduceDecisionResponse
from app.domain.exceptions.event_exception import EventException
from app.domain.services.decision_engine import DecisionEngine


class ProduceDecisionUseCase(UseCaseContract):
    def __init__(self, unit_of_work_factory: Callable[..., UnitOfWorkContract]) -> None:
        super().__init__(unit_of_work_factory=unit_of_work_factory)
        self.decision_engine = DecisionEngine()

    def execute(
        self, dto_request: DTOProduceDecisionRequest
    ) -> DTOProduceDecisionResponse:
        with self.unit_of_work_factory() as unit_of_work:
            event = unit_of_work.events.get_by_id(event_id=dto_request.event_id)
            if not event:
                raise EventException.event_not_found()
            rules = unit_of_work.rules.list_all()
            decision = self.decision_engine.decide(event=event, rules=rules)
            saved_decision = unit_of_work.decisions.save(decision=decision)

            return DTOProduceDecisionResponse(
                event_id=saved_decision.event_id,
                rule_id=saved_decision.rule_id,
                status=saved_decision.outcome,
                explanation=saved_decision.explanation,
                decision_id=saved_decision.id,
            )
