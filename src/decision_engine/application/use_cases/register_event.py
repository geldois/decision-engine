from __future__ import annotations

import structlog

from decision_engine.application.contracts.use_case import UseCase
from decision_engine.application.dto.requests.register_event import (
    RegisterEventDTORequest,
)
from decision_engine.application.dto.responses.register_event import (
    RegisterEventDTOResponse,
)
from decision_engine.domain.entities.event import Event

logger = structlog.get_logger()


class RegisterEventUseCase(UseCase[RegisterEventDTORequest, RegisterEventDTOResponse]):
    def execute(self, dto: RegisterEventDTORequest) -> RegisterEventDTOResponse:
        with self.uow_factory() as uow:
            event = Event(
                event_type=dto.event_type,
                payload=dto.payload,
                occurred_at=dto.occurred_at,
            )
            saved_event = uow.events.save(event=event)

            logger.info(
                "event.registered",
                event_id=str(saved_event.id),
                event_type=saved_event.event_type,
            )

            return RegisterEventDTOResponse(
                event_type=saved_event.event_type,
                payload=saved_event.payload,
                occurred_at=saved_event.occurred_at,
                event_id=saved_event.id,
            )
