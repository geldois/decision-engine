from collections.abc import Callable
from typing import cast

from app.api.mappers.http_error_code_mapper import (
    map_exception_to_http_exception,
)
from app.api.schemas.use_cases.http_register_rule_request import HTTPRegisterRuleRequest
from app.api.schemas.use_cases.http_register_rule_response import (
    HTTPRegisterRuleResponse,
)
from app.application.dto.dto_condition import DTOCondition
from app.application.dto.dto_register_rule_request import DTORegisterRuleRequest
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase


def build_register_rule_handler(
    register_rule_use_case: RegisterRuleUseCase,
) -> Callable[[HTTPRegisterRuleRequest], HTTPRegisterRuleResponse]:
    def register_rule_handler(
        http_register_rule_request: HTTPRegisterRuleRequest,
    ) -> HTTPRegisterRuleResponse:
        try:
            dto_register_rule_request = DTORegisterRuleRequest(
                name=http_register_rule_request.name,
                condition=cast(DTOCondition, http_register_rule_request.condition),
                outcome=http_register_rule_request.outcome,
                priority=http_register_rule_request.priority,
            )
            dto_register_rule_response = register_rule_use_case.execute(
                dto_request=dto_register_rule_request
            )

            return HTTPRegisterRuleResponse(
                name=dto_register_rule_response.name,
                condition=dto_register_rule_response.condition,
                outcome=dto_register_rule_response.outcome,
                priority=dto_register_rule_response.priority,
                rule_id=dto_register_rule_response.rule_id,
            )
        except Exception as exception:
            raise map_exception_to_http_exception(exception=exception) from exception

    return register_rule_handler
