from app.application.contracts.use_cases.use_case_contract import UseCaseContract
from app.application.dto.register_event_dto_request import RegisterEventDtoRequest
from app.application.dto.register_event_dto_response import RegisterEventDtoResponse
from app.domain.entities.events.event import Event


class RegisterEventUseCase(UseCaseContract):
    def execute(
        self, register_event_dto_request: RegisterEventDtoRequest
    ) -> RegisterEventDtoResponse:
        with self.unit_of_work_factory() as unit_of_work:
            event = Event(
                event_type=register_event_dto_request.event_type,
                payload=register_event_dto_request.payload,
                timestamp=register_event_dto_request.timestamp,
            )
            saved_event = unit_of_work.event_repository.save(event=event)

            return RegisterEventDtoResponse(
                event_type=saved_event.event_type,
                payload=saved_event.payload,
                timestamp=saved_event.timestamp,
                event_id=saved_event.id,
            )
