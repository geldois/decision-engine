from fastapi import APIRouter, HTTPException, status

from app.api.schemas.register_rule_http_request import RegisterRuleHttpRequest
from app.api.schemas.register_rule_http_response import RegisterRuleHttpResponse
from app.application.dto.register_rule_dto_request import RegisterRuleDtoRequest
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase


def create_rules_router(register_rule_use_case: RegisterRuleUseCase) -> APIRouter:
    rules_router = APIRouter()

    @rules_router.post("/rules", response_model=RegisterRuleHttpResponse)
    def register_rule(
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
            register_rule_dto_response = register_rule_use_case.register_rule(
                register_rule_dto_request=register_rule_dto_request
            )

            return RegisterRuleHttpResponse(
                name=register_rule_dto_response.name,
                outcome=register_rule_dto_response.outcome.value,
                rule_id=register_rule_dto_response.rule_id,
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

    return rules_router
