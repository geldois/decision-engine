from fastapi import APIRouter

from decision_engine.application.dto.requests.produce_decision import ProduceDecisionDTORequest
from decision_engine.config.container import Container
from decision_engine.interface.http.mappers.http_error_code_mapper import map_http_exception
from decision_engine.interface.http.schemas.requests.http_produce_decision_request import (
    HTTPProduceDecisionRequest,
)
from decision_engine.interface.http.schemas.responses.http_produce_decision_response import (
    HTTPProduceDecisionResponse,
)


def build_decision_router(container: Container) -> APIRouter:
    router = APIRouter(prefix="/decisions")

    @router.post("/", response_model=HTTPProduceDecisionResponse)
    def produce_decision(
        http_request: HTTPProduceDecisionRequest,
    ) -> HTTPProduceDecisionResponse:
        try:
            request = ProduceDecisionDTORequest(event_id=http_request.event_id)
            response = container.use_cases.produce_decision.execute(dto=request)

            return HTTPProduceDecisionResponse(
                event_id=response.event_id,
                rule_id=response.rule_id,
                status=response.status,
                traces=response.traces,
                decision_id=response.decision_id,
            )
        except Exception as exception:
            raise map_http_exception(exception=exception) from exception

    return router
