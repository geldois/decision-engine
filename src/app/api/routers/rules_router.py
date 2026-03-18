from typing import Callable

from fastapi import APIRouter

from app.api.schemas.register_rule_http_request import RegisterRuleHttpRequest
from app.api.schemas.register_rule_http_response import RegisterRuleHttpResponse


def build_rules_router(
    register_rule_handler: Callable[
        [RegisterRuleHttpRequest], RegisterRuleHttpResponse
    ],
) -> APIRouter:
    rules_router = APIRouter(prefix="/rules")

    @rules_router.post("/", response_model=RegisterRuleHttpResponse)
    def route(
        http_request: RegisterRuleHttpRequest,
    ) -> RegisterRuleHttpResponse:
        return register_rule_handler(http_request)

    return rules_router
