from collections.abc import Callable

from fastapi import APIRouter

from app.api.schemas.use_cases.http_register_event_request import (
    HTTPRegisterEventRequest,
)
from app.api.schemas.use_cases.http_register_event_response import (
    HTTPRegisterEventResponse,
)


def build_events_router(
    register_event_handler: Callable[
        [HTTPRegisterEventRequest], HTTPRegisterEventResponse
    ],
) -> APIRouter:
    events_router = APIRouter(prefix="/events")

    @events_router.post("/", response_model=HTTPRegisterEventResponse)
    def register_event(
        http_request: HTTPRegisterEventRequest,
    ) -> HTTPRegisterEventResponse:
        return register_event_handler(http_request)

    return events_router
