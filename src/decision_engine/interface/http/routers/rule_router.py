from typing import cast

from fastapi import APIRouter

from decision_engine.application.dto.condition import ConditionDTO  # noqa: TC001
from decision_engine.application.dto.requests.register_rule import (
    RegisterRuleDTORequest,
)
from decision_engine.config.container import Container
from decision_engine.interface.http.mappers.http_error_code_mapper import (
    map_http_exception,
)
from decision_engine.interface.http.schemas.requests.http_register_rule_request import (
    HTTPRegisterRuleRequest,
)
from decision_engine.interface.http.schemas.responses.http_register_rule_response import (  # noqa: E501
    HTTPRegisterRuleResponse,
)


def build_rule_router(container: Container) -> APIRouter:
    router = APIRouter(prefix="/rules")

    @router.get("/")
    def list_rules() -> list[HTTPRegisterRuleResponse]:  # pyright: ignore[reportUnusedFunction]
        try:
            response = container.use_cases.list_rules.execute(dto=None)

            return [
                HTTPRegisterRuleResponse(
                    name=r.name,
                    condition=r.condition,
                    outcome=r.outcome,
                    priority=r.priority,
                    rule_id=r.rule_id,
                )
                for r in response
            ]
        except Exception as exception:
            raise map_http_exception(exception=exception) from exception

    @router.post("/")
    def register_rule(  # pyright: ignore[reportUnusedFunction]
        http_request: HTTPRegisterRuleRequest,
    ) -> HTTPRegisterRuleResponse:
        try:
            request = RegisterRuleDTORequest(
                name=http_request.name,
                condition=cast("ConditionDTO", http_request.condition),
                outcome=http_request.outcome,
                priority=http_request.priority,
            )
            response = container.use_cases.register_rule.execute(dto=request)

            return HTTPRegisterRuleResponse(
                name=response.name,
                condition=response.condition,
                outcome=response.outcome,
                priority=response.priority,
                rule_id=response.rule_id,
            )
        except Exception as exception:
            raise map_http_exception(exception=exception) from exception

    return router
