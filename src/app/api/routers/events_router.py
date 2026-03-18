from fastapi import APIRouter

from app.api.handlers.register_event_handler import RegisterEventHandler
from app.api.schemas.register_event_http_request import RegisterEventHttpRequest
from app.api.schemas.register_event_http_response import RegisterEventHttpResponse


def events_router_factory(
    register_event_handler: RegisterEventHandler,
) -> APIRouter:
    events_router = APIRouter(prefix="/events")

    @events_router.post("/", response_model=RegisterEventHttpResponse)
    def route(
        register_event_http_request: RegisterEventHttpRequest,
    ) -> RegisterEventHttpResponse:
        return register_event_handler(
            register_event_http_request=register_event_http_request
        )

    return events_router
