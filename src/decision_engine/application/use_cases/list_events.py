from __future__ import annotations

import structlog

from decision_engine.application.contracts.use_case import UseCase
from decision_engine.application.dto.responses.register_event import (
    RegisterEventDTOResponse,
)

logger = structlog.get_logger()


class ListEventsUseCase(UseCase[None, list[RegisterEventDTOResponse]]):
    def execute(self, dto: None) -> list[RegisterEventDTOResponse]:  # noqa: ARG002
        with self.uow_factory() as uow:
            events = uow.events.list_all()

            logger.info("events.listed", count=len(events))

            return [
                RegisterEventDTOResponse(
                    event_type=event.event_type,
                    payload=event.payload,
                    occurred_at=event.occurred_at,
                    event_id=event.id,
                )
                for event in events
            ]
