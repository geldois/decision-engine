from fastapi import APIRouter, HTTPException, status

from app.api.schemas.register_event_http_request import RegisterEventHttpRequest
from app.api.schemas.register_event_http_response import RegisterEventHttpResponse
from app.application.dto.register_event_dto_request import RegisterEventDtoRequest
from app.application.use_cases.register_event_use_case import RegisterEventUseCase


def create_events_router(register_event_use_case: RegisterEventUseCase) -> APIRouter:
    events_router = APIRouter()

    @events_router.post("/events", response_model=RegisterEventHttpResponse)
    def register_event(
        register_event_http_request: RegisterEventHttpRequest,
    ) -> RegisterEventHttpResponse:
        try:
            register_event_dto_request = RegisterEventDtoRequest(
                event_type=register_event_http_request.event_type,
                payload=register_event_http_request.payload,
                timestamp=register_event_http_request.timestamp,
            )
            register_event_dto_response = register_event_use_case.register_event(
                register_event_dto_request=register_event_dto_request
            )

            return RegisterEventHttpResponse(
                event_type=register_event_dto_response.event_type,
                payload=register_event_dto_response.payload,
                timestamp=register_event_dto_response.timestamp,
                event_id=register_event_dto_response.event_id,
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return events_router
