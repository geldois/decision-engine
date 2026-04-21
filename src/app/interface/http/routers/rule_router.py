from typing import cast

from fastapi import APIRouter

from app.application.dto.dto_condition import DTOCondition
from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.config.container import Container
from app.interface.http.mappers.http_error_code_mapper import map_http_exception
from app.interface.http.schemas.requests.http_register_rule_request import (
    HTTPRegisterRuleRequest,
)
from app.interface.http.schemas.responses.http_register_rule_response import (
    HTTPRegisterRuleResponse,
)


def build_rule_router(container: Container) -> APIRouter:
    router = APIRouter(prefix="/rules")

    @router.post("/", response_model=HTTPRegisterRuleResponse)
    def register_rule(
        http_request: HTTPRegisterRuleRequest,
    ) -> HTTPRegisterRuleResponse:
        try:
            request = DTORegisterRuleRequest(
                name=http_request.name,
                condition=cast(DTOCondition, http_request.condition),
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
