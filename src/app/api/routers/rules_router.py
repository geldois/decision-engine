from collections.abc import Callable

from fastapi import APIRouter

from app.api.schemas.use_cases.http_register_rule_request import HTTPRegisterRuleRequest
from app.api.schemas.use_cases.http_register_rule_response import (
    HTTPRegisterRuleResponse,
)


def build_rules_router(
    register_rule_handler: Callable[
        [HTTPRegisterRuleRequest], HTTPRegisterRuleResponse
    ],
) -> APIRouter:
    rules_router = APIRouter(prefix="/rules")

    @rules_router.post("/", response_model=HTTPRegisterRuleResponse)
    def register_rule(
        http_request: HTTPRegisterRuleRequest,
    ) -> HTTPRegisterRuleResponse:
        return register_rule_handler(http_request)

    return rules_router
