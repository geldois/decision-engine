from collections.abc import Callable

from fastapi import HTTPException, status

from app.api.mappers.http_error_code_mapper import (
    map_domain_exception_to_http_error_code,
)
from app.api.schemas.http_error_response import HttpErrorResponse
from app.api.schemas.use_cases.register_rule_http_request import RegisterRuleHttpRequest
from app.api.schemas.use_cases.register_rule_http_response import (
    RegisterRuleHttpResponse,
)
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

        # ..........
        # tmp
        # ..........
        except ValueError as exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail={"error": "RULE_CONDITION_INVALID", "message": str(exception)},
            ) from exception
        # ..........

        except DomainException as exception:
            http_error_response = HttpErrorResponse(
                error=exception.exception_code,
                message=exception.message,
                details=exception.details,
            )

            raise HTTPException(
                status_code=map_domain_exception_to_http_error_code(exception),
                detail=http_error_response.model_dump(),
            ) from exception
        except Exception as exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from exception

    return register_rule_handler
