from fastapi import HTTPException, status

from app.api.schemas.produce_decision_http_request import ProduceDecisionHttpRequest
from app.api.schemas.produce_decision_http_response import ProduceDecisionHttpResponse
from app.application.dto.produce_decision_dto_request import ProduceDecisionDtoRequest
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase


class ProduceDecisionHandler:
    def __init__(self, produce_decision_use_case: ProduceDecisionUseCase) -> None:
        self.produce_decision_use_case = produce_decision_use_case

    def __call__(
        self, produce_decision_http_request: ProduceDecisionHttpRequest
    ) -> ProduceDecisionHttpResponse:
        try:
            produce_decision_dto_request = ProduceDecisionDtoRequest(
                event_id=produce_decision_http_request.event_id
            )
            produce_decision_dto_response = self.produce_decision_use_case.execute(
                dto_request=produce_decision_dto_request
            )

            return ProduceDecisionHttpResponse(
                event_id=produce_decision_dto_response.event_id,
                rule_id=produce_decision_dto_response.rule_id,
                status=produce_decision_dto_response.status.value,
                explanation=produce_decision_dto_response.explanation,
                decision_id=produce_decision_dto_response.decision_id,
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )
