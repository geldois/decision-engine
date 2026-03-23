from collections.abc import Callable
from dataclasses import dataclass

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.api.schemas.use_cases.http_produce_decision_request import (
    HTTPProduceDecisionRequest,
)
from app.api.schemas.use_cases.http_produce_decision_response import (
    HTTPProduceDecisionResponse,
)
from app.api.schemas.use_cases.http_register_event_request import (
    HTTPRegisterEventRequest,
)
from app.api.schemas.use_cases.http_register_event_response import (
    HTTPRegisterEventResponse,
)
from app.api.schemas.use_cases.http_register_rule_request import HTTPRegisterRuleRequest
from app.api.schemas.use_cases.http_register_rule_response import (
    HTTPRegisterRuleResponse,
)
from app.application.contracts.unit_of_work_contract import (
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
        [HTTPProduceDecisionRequest], HTTPProduceDecisionResponse
    ]
    register_event_handler: Callable[
        [HTTPRegisterEventRequest], HTTPRegisterEventResponse
    ]
    register_rule_handler: Callable[[HTTPRegisterRuleRequest], HTTPRegisterRuleResponse]

    # routers
    decisions_router: APIRouter
    events_router: APIRouter
    rules_router: APIRouter
