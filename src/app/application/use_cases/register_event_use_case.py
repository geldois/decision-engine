from app.application.contracts.use_case_contract import UseCaseContract
from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.application.dto.dto_register_event_response import DTORegisterEventResponse
from app.domain.entities.event import Event


class RegisterEventUseCase(UseCaseContract):
    def execute(self, dto_request: DTORegisterEventRequest) -> DTORegisterEventResponse:
        with self.unit_of_work_factory() as unit_of_work:
            event = Event(
                event_type=dto_request.event_type,
                payload=dto_request.payload,
                occurred_at=dto_request.occurred_at,
            )
            saved_event = unit_of_work.events.save(event=event)

            return DTORegisterEventResponse(
                event_type=saved_event.event_type,
                payload=saved_event.payload,
                occurred_at=saved_event.occurred_at,
                event_id=saved_event.id,
            )
