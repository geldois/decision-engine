from app.application.contracts.use_case import UseCase
from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.application.dto.dto_register_event_response import DTORegisterEventResponse
from app.domain.entities.event import Event


class RegisterEventUseCase(UseCase[DTORegisterEventRequest, DTORegisterEventResponse]):
    def execute(self, dto: DTORegisterEventRequest) -> DTORegisterEventResponse:
        with self.uow_factory() as uow:
            event = Event(
                event_type=dto.event_type,
                payload=dto.payload,
                occurred_at=dto.occurred_at,
            )
            saved_event = uow.events.save(event=event)

            return DTORegisterEventResponse(
                event_type=saved_event.event_type,
                payload=saved_event.payload,
                occurred_at=saved_event.occurred_at,
                event_id=saved_event.id,
            )
