from __future__ import annotations

import structlog

from decision_engine.application.contracts.use_case import UseCase
from decision_engine.application.dto.responses.produce_decision import (
    ProduceDecisionDTOResponse,
)
from decision_engine.application.presenters.decision_trace_presenter import (
    DecisionTracePresenter,
)

logger = structlog.get_logger()


class ListDecisionsUseCase(UseCase[None, list[ProduceDecisionDTOResponse]]):
    def execute(self, dto: None) -> list[ProduceDecisionDTOResponse]:  # noqa: ARG002
        with self.uow_factory() as uow:
            decisions = uow.decisions.list_all()

            logger.info("decisions.listed", count=len(decisions))

            return [
                ProduceDecisionDTOResponse(
                    event_id=decision.event_id,
                    rule_id=decision.rule_id,
                    status=decision.outcome.value,
                    traces=DecisionTracePresenter.present(element=decision.traces),
                    decision_id=decision.id,
                )
                for decision in decisions
            ]
