from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_produce_decision_use_case
from app.api.schemas.produce_decision_http_request import ProduceDecisionHttpRequest
from app.api.schemas.produce_decision_http_response import ProduceDecisionHttpResponse
from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase

router = APIRouter()

# routes
@router.post(
    "/events", 
    response_model = ProduceDecisionHttpResponse
)
def produce_decision(
    produce_decision_http_request: ProduceDecisionHttpRequest,
    produce_decision_use_case: ProduceDecisionUseCase = Depends(get_produce_decision_use_case)
) -> ProduceDecisionHttpResponse:
    try:
        produce_decision_dto_request = ProduceDecisionDtoRequest(
            event_type = produce_decision_http_request.event_type,
            payload = produce_decision_http_request.payload,
            timestamp = produce_decision_http_request.timestamp
        )
        produce_decision_dto_response = produce_decision_use_case.produce_decision(produce_decision_dto_request = produce_decision_dto_request)
        return ProduceDecisionHttpResponse(
            event_id = produce_decision_dto_response.event_id, 
            status = produce_decision_dto_response.status.value
        )
    except Exception as exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        ) from exception
    