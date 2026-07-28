from __future__ import annotations

from dotenv import load_dotenv

from alembic import command, config
from decision_engine.application.use_cases.list_decisions import ListDecisionsUseCase
from decision_engine.application.use_cases.list_events import ListEventsUseCase
from decision_engine.application.use_cases.list_rules import ListRulesUseCase
from decision_engine.application.use_cases.produce_decision import (
    ProduceDecisionUseCase,
)
from decision_engine.application.use_cases.register_event import RegisterEventUseCase
from decision_engine.application.use_cases.register_rule import RegisterRuleUseCase
from decision_engine.config.container import Container, ContainerOverride, UseCaseSet
from decision_engine.config.settings import Settings
from decision_engine.infrastructure.persistence.mem.db import MemDBBuilder
from decision_engine.infrastructure.persistence.sqlalchemy.db import SQLAlchemyDBBuilder


def load_environment() -> None:
    load_dotenv(override=False)


def run_migrations() -> None:
    alembic_config = config.Config("alembic.ini")
    command.upgrade(alembic_config, "head")


def build_container(
    settings: Settings | None = None, overrides: ContainerOverride | None = None
) -> Container:
    settings = settings or Settings.build()

    match settings.persistence:
        case "mem":
            db = (
                overrides.mem_db
                if overrides and overrides.mem_db
                else MemDBBuilder.build()
            )
        case "postgresql":
            db = (
                overrides.sqlalchemy_db
                if overrides and overrides.sqlalchemy_db
                else SQLAlchemyDBBuilder.build(settings=settings)
            )

    use_cases = UseCaseSet(
        produce_decision=ProduceDecisionUseCase(uow_factory=db.uow_factory),
        register_event=RegisterEventUseCase(uow_factory=db.uow_factory),
        register_rule=RegisterRuleUseCase(uow_factory=db.uow_factory),
        list_decisions=ListDecisionsUseCase(uow_factory=db.uow_factory),
        list_events=ListEventsUseCase(uow_factory=db.uow_factory),
        list_rules=ListRulesUseCase(uow_factory=db.uow_factory),
    )

    return Container(settings=settings, db=db, use_cases=use_cases)
