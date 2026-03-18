from typing import Callable

from fastapi import APIRouter

from app.api.schemas.register_event_http_request import RegisterEventHttpRequest
from app.api.schemas.register_event_http_response import RegisterEventHttpResponse


def build_events_router(
    register_event_handler: Callable[
        [RegisterEventHttpRequest], RegisterEventHttpResponse
    ],
) -> APIRouter:
    events_router = APIRouter(prefix="/events")

    @events_router.post("/", response_model=RegisterEventHttpResponse)
    def route(
        http_request: RegisterEventHttpRequest,
    ) -> RegisterEventHttpResponse:
        return register_event_handler(http_request)

    return events_router
