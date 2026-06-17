from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from decision_engine.application.protocols.db_protocol import DBProtocol
    from decision_engine.application.use_cases.list_decisions import (
        ListDecisionsUseCase,
    )
    from decision_engine.application.use_cases.list_events import ListEventsUseCase
    from decision_engine.application.use_cases.list_rules import ListRulesUseCase
    from decision_engine.application.use_cases.produce_decision import (
        ProduceDecisionUseCase,
    )
    from decision_engine.application.use_cases.register_event import (
        RegisterEventUseCase,
    )
    from decision_engine.application.use_cases.register_rule import RegisterRuleUseCase
    from decision_engine.config.settings import Settings
    from decision_engine.infrastructure.persistence.mem.db import MemDB
    from decision_engine.infrastructure.persistence.sqlalchemy.db import SQLAlchemyDB


@dataclass(frozen=True)
class UseCaseSet:
    produce_decision: ProduceDecisionUseCase
    register_event: RegisterEventUseCase
    register_rule: RegisterRuleUseCase
    list_decisions: ListDecisionsUseCase
    list_events: ListEventsUseCase
    list_rules: ListRulesUseCase


@dataclass(frozen=True)
class Container:
    settings: Settings
    db: DBProtocol
    use_cases: UseCaseSet


@dataclass(frozen=True)
class ContainerOverride:
    mem_db: MemDB | None = None
    sqlalchemy_db: SQLAlchemyDB | None = None
