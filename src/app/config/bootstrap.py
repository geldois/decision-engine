import os

from dotenv import load_dotenv

from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.config.container import Container, ContainerOverride, UseCaseSet
from app.config.settings import Settings
from app.infrastructure.persistence.in_memory.db import InMemoryDBBuilder
from app.infrastructure.persistence.sqlalchemy.db import SQLAlchemyDBBuilder


def load_environment() -> None:
    env = os.getenv("ENV", "dev")
    dotenv_file = f".env.{env}"

    load_dotenv(dotenv_file, override=False)


def run_migrations() -> None:
    from alembic import command, config

    alembic_config = config.Config("alembic.ini")
    command.upgrade(alembic_config, "head")


def build_container(
    settings: Settings | None = None, overrides: ContainerOverride | None = None
) -> Container:
    settings = settings or Settings.build()

    match settings.persistence:
        case "in_memory":
            db = (
                overrides.in_memory_db
                if overrides and overrides.in_memory_db
                else InMemoryDBBuilder.build()
            )
        case "postgresql":
            db = (
                overrides.sqlalchemy_db
                if overrides and overrides.sqlalchemy_db
                else SQLAlchemyDBBuilder.build(settings=settings)
            )

            if db.database_url != settings.database_url:
                raise RuntimeError(
                    "DATABASE_URL mismatch between settings and injected DB"
                )
        case _:
            raise RuntimeError(
                f"error building container | $PERSISTENCE: {settings.persistence}"
            )

    use_cases = UseCaseSet(
        produce_decision=ProduceDecisionUseCase(uow_factory=db.uow_factory),
        register_event=RegisterEventUseCase(uow_factory=db.uow_factory),
        register_rule=RegisterRuleUseCase(uow_factory=db.uow_factory),
    )

    return Container(settings=settings, db=db, use_cases=use_cases)
