from collections.abc import Callable

from fastapi import HTTPException, status

from app.api.schemas.register_rule_http_request import RegisterRuleHttpRequest
from app.api.schemas.register_rule_http_response import RegisterRuleHttpResponse
from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.domain.exceptions.domain_exception import DomainException


def build_register_rule_handler(
    register_rule_use_case: RegisterRuleUseCase,
) -> Callable[[RegisterRuleHttpRequest], RegisterRuleHttpResponse]:
    def register_rule_handler(
        register_rule_http_request: RegisterRuleHttpRequest,
    ) -> RegisterRuleHttpResponse:
        try:
            register_rule_dto_request = RegisterRuleDtoRequest(
                name=register_rule_http_request.name,
                condition_field=register_rule_http_request.condition_field,
                condition_operator=register_rule_http_request.condition_operator,
                condition_value=register_rule_http_request.condition_value,
                outcome=register_rule_http_request.outcome,
            )
            register_rule_dto_response = register_rule_use_case.execute(
                dto_request=register_rule_dto_request
            )

            return RegisterRuleHttpResponse(
                name=register_rule_dto_response.name,
                outcome=register_rule_dto_response.outcome.value,
                rule_id=register_rule_dto_response.rule_id,
            )
        except DomainException as domain_exception:
            raise domain_exception
        except Exception as exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from exception

    return register_rule_handler
