from collections.abc import Callable

from app.api.mappers.http_error_code_mapper import (
    map_exception_to_http_exception,
)
from app.api.schemas.use_cases.http_produce_decision_request import (
    HTTPProduceDecisionRequest,
)
from app.api.schemas.use_cases.http_produce_decision_response import (
    HTTPProduceDecisionResponse,
)
from app.application.dto.dto_produce_decision_request import DTOProduceDecisionRequest
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase


def build_produce_decision_handler(
    produce_decision_use_case: ProduceDecisionUseCase,
) -> Callable[[HTTPProduceDecisionRequest], HTTPProduceDecisionResponse]:
    def produce_decision_handler(
        http_produce_decision_request: HTTPProduceDecisionRequest,
    ) -> HTTPProduceDecisionResponse:
        try:
            dto_produce_decision_request = DTOProduceDecisionRequest(
                event_id=http_produce_decision_request.event_id
            )
            dto_produce_decision_response = produce_decision_use_case.execute(
                dto_request=dto_produce_decision_request
            )

            return HTTPProduceDecisionResponse(
                event_id=dto_produce_decision_response.event_id,
                rule_id=dto_produce_decision_response.rule_id,
                status=dto_produce_decision_response.status.value,
                explanation=dto_produce_decision_response.explanation,
                decision_id=dto_produce_decision_response.decision_id,
            )
        except Exception as exception:
            raise map_exception_to_http_exception(exception=exception) from exception

    return produce_decision_handler
