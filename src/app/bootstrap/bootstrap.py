from functools import partial
from typing import Callable

from fastapi import FastAPI
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker

from app.api.handlers.produce_decision_handler import build_produce_decision_handler
from app.api.handlers.register_event_handler import build_register_event_handler
from app.api.handlers.register_rule_handler import build_register_rule_handler
from app.api.routers.decisions_router import build_decisions_router
from app.api.routers.events_router import build_events_router
from app.api.routers.rules_router import build_rules_router
from app.application.use_cases.produce_decision_use_case import (
    ProduceDecisionUseCase,
)
from app.application.use_cases.register_event_use_case import (
    RegisterEventUseCase,
)
from app.application.use_cases.register_rule_use_case import (
    RegisterRuleUseCase,
)
from app.bootstrap.container import Container
from app.infrastructure.database.base import Base
from app.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    InMemoryDecisionRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)
from app.infrastructure.persistence.in_memory.unit_of_work.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)
from app.infrastructure.persistence.sql.repositories.sql_decision_repository import (
    SqlDecisionRepository,
)
from app.infrastructure.persistence.sql.repositories.sql_event_repository import (
    SqlEventRepository,
)
from app.infrastructure.persistence.sql.repositories.sql_rule_repository import (
    SqlRuleRepository,
)
from app.infrastructure.persistence.sql.unit_of_work.sql_unit_of_work import (
    SqlUnitOfWork,
)


def build_in_memory_storage() -> InMemoryStorage:
    return InMemoryStorage()


def build_in_memory_unit_of_work_factory(
    in_memory_storage: InMemoryStorage,
) -> Callable[[], InMemoryUnitOfWork]:
    return partial(
        InMemoryUnitOfWork,
        in_memory_storage=in_memory_storage,
        decision_repository_factory=InMemoryDecisionRepository,
        event_repository_factory=InMemoryEventRepository,
        rule_repository_factory=InMemoryRuleRepository,
    )


def build_prod_session_factory() -> Callable[[], Session]:
    engine = create_engine(
        url="sqlite:///./db-prod.db", connect_args={"check_same_thread": True}
    )
    Base.metadata.create_all(bind=engine)

    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def build_dev_session_factory() -> Callable[[], Session]:
    engine = create_engine(
        url="sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)

    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def build_sql_unit_of_work_factory(
    session_factory: Callable[[], Session],
) -> Callable[[], SqlUnitOfWork]:
    return partial(
        SqlUnitOfWork,
        session_factory=session_factory,
        decision_repository_factory=SqlDecisionRepository,
        event_repository_factory=SqlEventRepository,
        rule_repository_factory=SqlRuleRepository,
    )


def bootstrap(env: str) -> Container:
    if env in "prod" or env == "dev":
        in_memory_storage = None
        session_factory = (
            build_prod_session_factory()
            if env == "prod"
            else build_dev_session_factory()
        )
        unit_of_work_factory = build_sql_unit_of_work_factory(
            session_factory=session_factory
        )
    elif env == "test":
        in_memory_storage = InMemoryStorage()
        session_factory = build_dev_session_factory()
        unit_of_work_factory = build_in_memory_unit_of_work_factory(
            in_memory_storage=in_memory_storage
        )
    else:
        raise ValueError("invalid env")

    return Container(
        in_memory_storage=in_memory_storage,
        session_factory=session_factory,
        unit_of_work_factory=unit_of_work_factory,
    )


def create_app(container: Container) -> FastAPI:
    app = FastAPI()

    # use cases
    produce_decision_use_case = ProduceDecisionUseCase(
        unit_of_work_factory=container.unit_of_work_factory
    )
    register_event_use_case = RegisterEventUseCase(
        unit_of_work_factory=container.unit_of_work_factory
    )
    register_rule_use_case = RegisterRuleUseCase(
        unit_of_work_factory=container.unit_of_work_factory
    )

    # handlers
    produce_decision_handler = build_produce_decision_handler(
        produce_decision_use_case=produce_decision_use_case
    )
    register_event_handler = build_register_event_handler(
        register_event_use_case=register_event_use_case
    )
    register_rule_handler = build_register_rule_handler(
        register_rule_use_case=register_rule_use_case
    )

    # routers
    decisions_router = build_decisions_router(
        produce_decision_handler=produce_decision_handler
    )
    events_router = build_events_router(register_event_handler=register_event_handler)
    rules_router = build_rules_router(register_rule_handler=register_rule_handler)

    # app config
    app.include_router(decisions_router)
    app.include_router(events_router)
    app.include_router(rules_router)

    return app
