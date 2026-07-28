from __future__ import annotations

import os
from collections.abc import Callable, Generator
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.orm import Session

from alembic import command, config
from decision_engine.config.bootstrap import build_container, load_environment
from decision_engine.config.container import Container, ContainerOverride
from decision_engine.config.settings import Settings
from decision_engine.domain.entities.decision import Decision
from decision_engine.domain.entities.event import Event
from decision_engine.domain.entities.rule import Rule
from decision_engine.domain.services.decision_engine import DecisionEngine
from decision_engine.domain.value_objects.condition import Condition, SimpleCondition
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome
from decision_engine.domain.value_objects.decision_trace import SimpleDecisionTrace
from decision_engine.domain.value_objects.event_field import EventField
from decision_engine.domain.value_objects.operators.comparison_operator import (
    ComparisonOperator,
)
from decision_engine.infrastructure.config.db import build_database_url
from decision_engine.infrastructure.persistence.mem.db import MemDB
from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage
from decision_engine.infrastructure.persistence.mem.mem_uow import MemUoW
from decision_engine.infrastructure.persistence.sqlalchemy.db import SQLAlchemyDB
from decision_engine.infrastructure.persistence.sqlalchemy.sqlalchemy_uow import (
    SQLAlchemyUoW,
)
from decision_engine.interface.http.app import create_app

if TYPE_CHECKING:
    from fastapi import FastAPI

type MakeDecision = Callable[..., Decision]
type MakeEvent = Callable[..., Event]
type MakeRule = Callable[..., Rule]
type MakeSimpleCondition = Callable[..., SimpleCondition]
type MakeSimpleDecisionTrace = Callable[..., SimpleDecisionTrace]


@pytest.fixture
def make_decision() -> MakeDecision:
    def decision(*, event: Event, rules: list[Rule]) -> Decision:
        return DecisionEngine.decide(event=event, rules=rules)

    return decision


@pytest.fixture
def make_event() -> MakeEvent:
    def event(
        *,
        event_type: str = "TEST",
        payload: dict[str, object] | None = None,
        occurred_at: int = 1000000000,
    ) -> Event:
        return Event(
            event_type=event_type,
            payload=payload if payload is not None else {"test": True, "info": "TEST"},
            occurred_at=occurred_at,
        )

    return event


@pytest.fixture
def make_rule(make_simple_condition: MakeSimpleCondition) -> MakeRule:
    def rule(
        *,
        name: str = "TEST",
        condition: Condition | None = None,
        outcome: DecisionOutcome = DecisionOutcome.APPROVED,
        priority: int = 0,
    ) -> Rule:
        return Rule(
            name=name,
            condition=condition if condition is not None else make_simple_condition(),
            outcome=outcome,
            priority=priority,
        )

    return rule


@pytest.fixture
def make_simple_condition() -> MakeSimpleCondition:
    def simple_condition(
        *,
        operator: ComparisonOperator = ComparisonOperator.EQUALS,
        field: EventField = EventField.EVENT_TYPE,
        value: object = "TEST",
    ) -> SimpleCondition:
        return SimpleCondition(operator=operator, field=field, value=value)

    return simple_condition


@pytest.fixture
def make_simple_decision_trace() -> MakeSimpleDecisionTrace:
    def simple_decision_trace(
        *,
        result: bool = False,
        operator: ComparisonOperator = ComparisonOperator.EQUALS,
        field: EventField = EventField.EVENT_TYPE,
        expected_value: object = "USER_CREATED",
        actual_value: object = "TEST",
    ) -> SimpleDecisionTrace:
        return SimpleDecisionTrace(
            result=result,
            operator=operator,
            field=field,
            expected_value=expected_value,
            actual_value=actual_value,
        )

    return simple_decision_trace


@pytest.fixture(scope="session")
def setup_environment() -> Generator[None, None, None]:
    old_env = os.getenv("ENV")

    os.environ["ENV"] = "test"

    load_environment()

    yield

    if old_env is None:
        del os.environ["ENV"]
    else:
        os.environ["ENV"] = old_env


@pytest.fixture(params=["mem", "postgresql"])
def persistence(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture
def settings(setup_environment: None, persistence: str) -> Settings:  # noqa: ARG001
    env = os.getenv("ENV")
    db_prefix = os.getenv("DB_PREFIX")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    return Settings.build(
        env=env,
        persistence=persistence,
        db_prefix=db_prefix,
        db_user=db_user,
        db_pass=db_pass,
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
    )


@pytest.fixture(scope="session")
def setup_migrations(setup_environment: None) -> Generator[None, None, None]:  # noqa: ARG001
    alembic_config = config.Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", build_database_url())

    command.upgrade(alembic_config, "head")

    yield

    command.downgrade(alembic_config, "base")


@pytest.fixture
def mem_storage() -> Generator[MemStorage, None, None]:
    storage = MemStorage()

    yield storage

    storage.clear()


@pytest.fixture
def mem_uow_factory(
    mem_storage: MemStorage,
) -> Callable[[], MemUoW]:
    return lambda: MemUoW(storage=mem_storage)


@pytest.fixture
def mem_db(
    mem_uow_factory: Callable[[], MemUoW],
    mem_storage: MemStorage,
) -> MemDB:
    return MemDB(uow_factory=mem_uow_factory, storage=mem_storage)


@pytest.fixture
def engine(setup_migrations: None) -> Generator[Engine, None, None]:  # noqa: ARG001
    engine = create_engine(url=build_database_url())

    yield engine

    engine.dispose()


@pytest.fixture
def connection(engine: Engine) -> Generator[Connection, None, None]:
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture
def session(connection: Connection) -> Generator[Session, None, None]:
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    if session:
        session.close()


@pytest.fixture
def sqlalchemy_uow_factory(
    session: Session,
) -> Callable[[], SQLAlchemyUoW]:
    return lambda: SQLAlchemyUoW(session_factory=lambda: session)


@pytest.fixture
def sqlalchemy_db(
    connection: Connection,
    session: Session,
    sqlalchemy_uow_factory: Callable[[], SQLAlchemyUoW],
) -> SQLAlchemyDB:
    return SQLAlchemyDB(
        uow_factory=sqlalchemy_uow_factory,
        database_url=build_database_url(),
        engine=connection.engine,
        session_factory=lambda: session,
    )


@pytest.fixture
def container_override(
    settings: Settings, request: pytest.FixtureRequest
) -> ContainerOverride:
    match settings.persistence:
        case "mem":
            return ContainerOverride(mem_db=request.getfixturevalue("mem_db"))
        case "postgresql":
            return ContainerOverride(
                sqlalchemy_db=request.getfixturevalue("sqlalchemy_db")
            )


@pytest.fixture
def container(settings: Settings, container_override: ContainerOverride) -> Container:
    return build_container(settings=settings, overrides=container_override)


@pytest.fixture
def fastapi_app(container: Container) -> FastAPI:
    return create_app(container=container)


@pytest.fixture
def fastapi_testclient(fastapi_app: FastAPI) -> TestClient:
    return TestClient(app=fastapi_app, raise_server_exceptions=False)
