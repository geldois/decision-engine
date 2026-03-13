from collections.abc import Callable
from dataclasses import dataclass

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.api.schemas.produce_decision_http_request import ProduceDecisionHttpRequest
from app.api.schemas.produce_decision_http_response import ProduceDecisionHttpResponse
from app.api.schemas.register_event_http_request import RegisterEventHttpRequest
from app.api.schemas.register_event_http_response import RegisterEventHttpResponse
from app.api.schemas.register_rule_http_request import RegisterRuleHttpRequest
from app.api.schemas.register_rule_http_response import RegisterRuleHttpResponse
from app.application.contracts.unit_of_works.unit_of_work_contract import (
    UnitOfWorkContract,
)
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)


@dataclass
class Container:
    in_memory_storage: InMemoryStorage | None
    session_factory: Callable[[], Session] | None
    unit_of_work_factory: Callable[[], UnitOfWorkContract]

    # use cases
    produce_decision_use_case: ProduceDecisionUseCase
    register_event_use_case: RegisterEventUseCase
    register_rule_use_case: RegisterRuleUseCase

    # handlers
    produce_decision_handler: Callable[
        [ProduceDecisionHttpRequest], ProduceDecisionHttpResponse
    ]
    register_event_handler: Callable[
        [RegisterEventHttpRequest], RegisterEventHttpResponse
    ]
    register_rule_handler: Callable[[RegisterRuleHttpRequest], RegisterRuleHttpResponse]

    # routers
    decisions_router: APIRouter
    events_router: APIRouter
    rules_router: APIRouter
