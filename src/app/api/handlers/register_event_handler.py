from collections.abc import Callable

from app.api.mappers.http_error_code_mapper import (
    map_exception_to_http_exception,
)
from app.api.schemas.use_cases.http_register_event_request import (
    HTTPRegisterEventRequest,
)
from app.api.schemas.use_cases.http_register_event_response import (
    HTTPRegisterEventResponse,
)
from app.application.dto.dto_register_event_request import DTORegisterEventRequest
from app.application.use_cases.register_event_use_case import RegisterEventUseCase


def build_register_event_handler(
    register_event_use_case: RegisterEventUseCase,
) -> Callable[[HTTPRegisterEventRequest], HTTPRegisterEventResponse]:
    def register_event_handler(
        http_register_event_request: HTTPRegisterEventRequest,
    ) -> HTTPRegisterEventResponse:
        try:
            dto_register_event_request = DTORegisterEventRequest(
                event_type=http_register_event_request.event_type,
                payload=http_register_event_request.payload,
                occurred_at=http_register_event_request.occurred_at,
            )
            dto_register_event_response = register_event_use_case.execute(
                dto=dto_register_event_request
            )

            return HTTPRegisterEventResponse(
                event_type=dto_register_event_response.event_type,
                payload=dto_register_event_response.payload,
                occurred_at=dto_register_event_response.occurred_at,
                event_id=dto_register_event_response.event_id,
            )
        except Exception as exception:
            raise map_exception_to_http_exception(exception=exception) from exception

    return register_event_handler
