from collections.abc import Callable

from fastapi import APIRouter

from app.api.schemas.produce_decision_http_request import ProduceDecisionHttpRequest
from app.api.schemas.produce_decision_http_response import ProduceDecisionHttpResponse


def build_decisions_router(
    produce_decision_handler: Callable[
        [ProduceDecisionHttpRequest], ProduceDecisionHttpResponse
    ],
) -> APIRouter:
    decisions_router = APIRouter(prefix="/decisions")

    @decisions_router.post("/", response_model=ProduceDecisionHttpResponse)
    def produce_decision(http_request: ProduceDecisionHttpRequest) -> ProduceDecisionHttpResponse:
        return produce_decision_handler(http_request)

    return decisions_router
