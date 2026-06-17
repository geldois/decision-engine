from __future__ import annotations

import structlog

from decision_engine.application.contracts.use_case import UseCase
from decision_engine.application.dto.requests.produce_decision import (
    ProduceDecisionDTORequest,
)
from decision_engine.application.dto.responses.produce_decision import (
    ProduceDecisionDTOResponse,
)
from decision_engine.application.presenters.decision_trace_presenter import (
    DecisionTracePresenter,
)
from decision_engine.domain.errors.event_error import NotFoundEventError
from decision_engine.domain.services.decision_engine import DecisionEngine

logger = structlog.get_logger()


class ProduceDecisionUseCase(
    UseCase[ProduceDecisionDTORequest, ProduceDecisionDTOResponse]
):
    def execute(self, dto: ProduceDecisionDTORequest) -> ProduceDecisionDTOResponse:
        with self.uow_factory() as uow:
            event = uow.events.get_by_id(event_id=dto.event_id)

            if not event:
                raise NotFoundEventError(event_id=dto.event_id)

            rules = uow.rules.list_all()
            decision = DecisionEngine.decide(event=event, rules=rules)
            saved_decision = uow.decisions.save(decision=decision)

            logger.info(
                "decision.produced",
                event_id=str(saved_decision.event_id),
                rule_id=str(saved_decision.rule_id) if saved_decision.rule_id else None,
                outcome=saved_decision.outcome.value,
            )

            return ProduceDecisionDTOResponse(
                event_id=saved_decision.event_id,
                rule_id=saved_decision.rule_id,
                status=saved_decision.outcome.value,
                traces=DecisionTracePresenter.present(element=saved_decision.traces),
                decision_id=saved_decision.id,
            )
