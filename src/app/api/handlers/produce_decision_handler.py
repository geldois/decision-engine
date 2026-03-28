from collections.abc import Callable

from fastapi import HTTPException, status

from app.api.mappers.http_error_code_mapper import (
    map_domain_exception_to_http_error_code,
)
from app.api.schemas.http_error_response import HttpErrorResponse
from app.api.schemas.use_cases.produce_decision_http_request import (
    ProduceDecisionHttpRequest,
)
from app.api.schemas.use_cases.produce_decision_http_response import (
    ProduceDecisionHttpResponse,
)
from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.domain.exceptions.domain_exception import DomainException


def build_produce_decision_handler(
    produce_decision_use_case: ProduceDecisionUseCase,
) -> Callable[[ProduceDecisionHttpRequest], ProduceDecisionHttpResponse]:
    def produce_decision_handler(
        produce_decision_http_request: ProduceDecisionHttpRequest,
    ) -> ProduceDecisionHttpResponse:
        try:
            produce_decision_dto_request = ProduceDecisionDtoRequest(
                event_id=produce_decision_http_request.event_id
            )
            produce_decision_dto_response = produce_decision_use_case.execute(
                dto_request=produce_decision_dto_request
            )

            return ProduceDecisionHttpResponse(
                event_id=produce_decision_dto_response.event_id,
                rule_id=produce_decision_dto_response.rule_id,
                status=produce_decision_dto_response.status.value,
                explanation=produce_decision_dto_response.explanation,
                decision_id=produce_decision_dto_response.decision_id,
            )
        except DomainException as exception:
            http_error_response = HttpErrorResponse(
                error=exception.exception_code,
                message=exception.message,
                details=exception.details,
            )

            raise HTTPException(
                status_code=map_domain_exception_to_http_error_code(exception),
                detail=http_error_response.model_dump(),
            ) from exception
        except Exception as exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from exception

    return produce_decision_handler
