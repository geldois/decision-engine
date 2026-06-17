from __future__ import annotations

from fastapi import APIRouter

from decision_engine.application.dto.requests.register_event import (
    RegisterEventDTORequest,
)
from decision_engine.config.container import Container
from decision_engine.interface.http.mappers.http_error_code_mapper import (
    map_http_exception,
)
from decision_engine.interface.http.schemas.requests.http_register_event_request import (
    HTTPRegisterEventRequest,
)
from decision_engine.interface.http.schemas.responses.http_register_event_response import (
    HTTPRegisterEventResponse,
)


def build_event_router(container: Container) -> APIRouter:
    router = APIRouter(prefix="/events")

    @router.post("/", response_model=HTTPRegisterEventResponse)
    def register_event(  # pyright: ignore[reportUnusedFunction]
        http_request: HTTPRegisterEventRequest,
    ) -> HTTPRegisterEventResponse:
        try:
            request = RegisterEventDTORequest(
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
