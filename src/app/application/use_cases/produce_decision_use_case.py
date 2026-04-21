from app.application.contracts.use_case import UseCase
from app.application.dto.dto_produce_decision_request import DTOProduceDecisionRequest
from app.application.dto.dto_produce_decision_response import DTOProduceDecisionResponse
from app.application.presenters.decision_trace_presenter import DecisionTracePresenter
from app.domain.exceptions.event_exception import EventException
from app.domain.services.decision_engine import DecisionEngine


class ProduceDecisionUseCase(
    UseCase[DTOProduceDecisionRequest, DTOProduceDecisionResponse]
):
    def execute(self, dto: DTOProduceDecisionRequest) -> DTOProduceDecisionResponse:
        with self.uow_factory() as uow:
            event = uow.events.get_by_id(event_id=dto.event_id)

            if not event:
                raise EventException.event_not_found()

            rules = uow.rules.list_all()
            decision = DecisionEngine.decide(event=event, rules=rules)
            saved_decision = uow.decisions.save(decision=decision)

            return DTOProduceDecisionResponse(
                event_id=saved_decision.event_id,
                rule_id=saved_decision.rule_id,
                status=saved_decision.outcome.value,
                traces=DecisionTracePresenter.present(element=saved_decision.traces),
                decision_id=saved_decision.id,
            )
