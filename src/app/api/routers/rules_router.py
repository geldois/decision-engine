from fastapi import APIRouter

from app.api.handlers.register_rule_handler import RegisterRuleHandler
from app.api.schemas.register_rule_http_request import RegisterRuleHttpRequest
from app.api.schemas.register_rule_http_response import RegisterRuleHttpResponse


def rules_router_factory(register_rule_handler: RegisterRuleHandler) -> APIRouter:
    rules_router = APIRouter(prefix="/rules")

    @rules_router.post("/", response_model=RegisterRuleHttpResponse)
    def route(
        register_rule_http_request: RegisterRuleHttpRequest,
    ) -> RegisterRuleHttpResponse:
        return register_rule_handler(
            register_rule_http_request=register_rule_http_request
        )

    return rules_router
