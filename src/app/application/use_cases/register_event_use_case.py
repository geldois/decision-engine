from app.application.dto.register_event_dto_request import RegisterEventDtoRequest
from app.application.dto.register_event_dto_response import RegisterEventDtoResponse
from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.domain.entities.events.event import Event

class RegisterEventUseCase:
    # initializer
    def __init__(
        self, 
        event_repository: EventRepositoryContract
    ):
        self.event_repository = event_repository

    # methods
    def register_event(
        self, 
        register_event_dto_request: RegisterEventDtoRequest
    ) -> RegisterEventDtoResponse:
        event = Event(
            event_type = register_event_dto_request.event_type, 
            payload = register_event_dto_request.payload, 
            timestamp = register_event_dto_request.timestamp
        )
        saved_event = self.event_repository.save(event)

        return RegisterEventDtoResponse(
            event_type = saved_event.event_type, 
            payload = saved_event.payload, 
            timestamp = saved_event.timestamp, 
            event_id = saved_event._id
        )
    