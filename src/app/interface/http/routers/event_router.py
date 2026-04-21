from fastapi import APIRouter

from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.config.container import Container
from app.interface.http.mappers.http_error_code_mapper import map_http_exception
from app.interface.http.schemas.requests.http_register_event_request import (
    HTTPRegisterEventRequest,
)
from app.interface.http.schemas.responses.http_register_event_response import (
    HTTPRegisterEventResponse,
)


def build_event_router(container: Container) -> APIRouter:
    router = APIRouter(prefix="/events")

    @router.post("/", response_model=HTTPRegisterEventResponse)
    def register_event(
        http_request: HTTPRegisterEventRequest,
    ) -> HTTPRegisterEventResponse:
        try:
            request = DTORegisterEventRequest(
                event_type=http_request.event_type,
                payload=http_request.payload,
                occurred_at=http_request.occurred_at,
            )
            response = container.use_cases.register_event.execute(dto=request)

            return HTTPRegisterEventResponse(
                event_type=response.event_type,
                payload=response.payload,
                occurred_at=response.occurred_at,
                event_id=response.event_id,
            )
        except Exception as exception:
            raise map_http_exception(exception=exception) from exception

    return router
