from dataclasses import dataclass

from app.application.protocols.db_protocol import DBProtocol
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.config.settings import Settings
from app.infrastructure.persistence.in_memory.db import InMemoryDB
from app.infrastructure.persistence.sqlalchemy.db import SQLAlchemyDB


@dataclass(frozen=True)
class UseCaseSet:
    produce_decision: ProduceDecisionUseCase
    register_event: RegisterEventUseCase
    register_rule: RegisterRuleUseCase


@dataclass(frozen=True)
class Container:
    settings: Settings
    db: DBProtocol
    use_cases: UseCaseSet


@dataclass(frozen=True)
class ContainerOverride:
    in_memory_db: InMemoryDB | None = None
    sqlalchemy_db: SQLAlchemyDB | None = None
