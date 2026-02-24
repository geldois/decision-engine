from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_register_event_use_case
from app.api.schemas.register_event_http_request import RegisterEventHttpRequest
from app.api.schemas.register_event_http_response import RegisterEventHttpResponse
from app.application.dto.register_event_request import RegisterEventRequest
from app.application.use_cases.register_event_use_case import RegisterEventUseCase

router = APIRouter()

@router.post(
    "/events", 
    response_model = RegisterEventHttpResponse
)
def register_event(
    request: RegisterEventHttpRequest,
    use_case: RegisterEventUseCase = Depends(get_register_event_use_case)
) -> RegisterEventHttpResponse:
    try:
        register_event_request = RegisterEventRequest(
            event_type = request.event_type,
            payload = request.payload,
            timestamp = request.timestamp
        )
        response = use_case.register_event(register_event_request)
        return RegisterEventHttpResponse(
            event_id = str(response.event_id), 
            status = response.status.value
        )
    except Exception as exc:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        ) from exc
    