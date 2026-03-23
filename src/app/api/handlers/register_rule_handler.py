from collections.abc import Callable

from app.api.mappers.http_error_code_mapper import (
    map_exception_to_http_exception,
)
from app.api.schemas.use_cases.http_register_rule_request import HTTPRegisterRuleRequest
from app.api.schemas.use_cases.http_register_rule_response import (
    HTTPRegisterRuleResponse,
)
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
                condition_field=http_register_rule_request.condition_field,
                condition_operator=http_register_rule_request.condition_operator,
                condition_value=http_register_rule_request.condition_value,
                outcome=http_register_rule_request.outcome,
            )
            dto_register_rule_response = register_rule_use_case.execute(
                dto_request=dto_register_rule_request
            )

            return HTTPRegisterRuleResponse(
                name=dto_register_rule_response.name,
                outcome=dto_register_rule_response.outcome.value,
                rule_id=dto_register_rule_response.rule_id,
            )
        except Exception as exception:
            raise map_exception_to_http_exception(exception=exception) from exception

    return register_rule_handler
