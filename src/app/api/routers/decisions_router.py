from fastapi import APIRouter

from app.api.handlers.produce_decision_handler import ProduceDecisionHandler
from app.api.schemas.produce_decision_http_request import ProduceDecisionHttpRequest
from app.api.schemas.produce_decision_http_response import ProduceDecisionHttpResponse


def decisions_router_factory(
    produce_decision_handler: ProduceDecisionHandler,
) -> APIRouter:
    decisions_router = APIRouter(prefix="/decisions")

    @decisions_router.post("/", response_model=ProduceDecisionHttpResponse)
    def route(
        produce_decision_http_request: ProduceDecisionHttpRequest,
    ) -> ProduceDecisionHttpResponse:
        return produce_decision_handler(
            produce_decision_http_request=produce_decision_http_request
        )

    return decisions_router
