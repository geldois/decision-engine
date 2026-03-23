from collections.abc import Callable

from fastapi import APIRouter

from app.api.schemas.use_cases.http_produce_decision_request import (
    HTTPProduceDecisionRequest,
)
from app.api.schemas.use_cases.http_produce_decision_response import (
    HTTPProduceDecisionResponse,
)


def build_decisions_router(
    produce_decision_handler: Callable[
        [HTTPProduceDecisionRequest], HTTPProduceDecisionResponse
    ],
) -> APIRouter:
    decisions_router = APIRouter(prefix="/decisions")

    @decisions_router.post("/", response_model=HTTPProduceDecisionResponse)
    def produce_decision(
        http_request: HTTPProduceDecisionRequest,
    ) -> HTTPProduceDecisionResponse:
        return produce_decision_handler(http_request)

    return decisions_router
