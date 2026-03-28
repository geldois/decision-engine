from collections.abc import Callable

from fastapi import APIRouter

from app.api.schemas.use_cases.register_rule_http_request import RegisterRuleHttpRequest
from app.api.schemas.use_cases.register_rule_http_response import (
    RegisterRuleHttpResponse,
)


def build_rules_router(
    register_rule_handler: Callable[
        [RegisterRuleHttpRequest], RegisterRuleHttpResponse
    ],
) -> APIRouter:
    rules_router = APIRouter(prefix="/rules")

    @rules_router.post("/", response_model=RegisterRuleHttpResponse)
    def register_rule(
        http_request: RegisterRuleHttpRequest,
    ) -> RegisterRuleHttpResponse:
        return register_rule_handler(http_request)

    return rules_router
