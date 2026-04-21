import os
from collections.abc import Callable, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.orm import Session

from app.config.bootstrap import build_container, load_environment
from app.config.container import Container, ContainerOverride
from app.config.settings import Settings
from app.infrastructure.config.db import build_database_url
from app.infrastructure.persistence.in_memory.db import InMemoryDB
from app.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage
from app.infrastructure.persistence.in_memory.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)
from app.infrastructure.persistence.sqlalchemy.db import SQLAlchemyDB
from app.infrastructure.persistence.sqlalchemy.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)
from app.interface.http.app import create_app

pytest_plugins = [
    "tests.fixtures.condition",
    "tests.fixtures.decision",
    "tests.fixtures.decision_trace",
    "tests.fixtures.event",
    "tests.fixtures.rule",
]


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


@pytest.fixture(scope="function", params=["in_memory", "postgresql"])
def persistence(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(scope="function")
def settings(setup_environment: None, persistence: str) -> Settings:
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
def setup_migrations(setup_environment: None) -> Generator[None, None, None]:
    from alembic import command, config

    alembic_config = config.Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", build_database_url())

    command.upgrade(alembic_config, "head")

    yield

    command.downgrade(alembic_config, "base")


@pytest.fixture(scope="function")
def in_memory_storage() -> Generator[InMemoryStorage, None, None]:
    storage = InMemoryStorage()

    yield storage

    storage.clear()


@pytest.fixture(scope="function")
def in_memory_uow_factory(
    in_memory_storage: InMemoryStorage,
) -> Callable[[], InMemoryUnitOfWork]:
    return lambda: InMemoryUnitOfWork(storage=in_memory_storage)


@pytest.fixture(scope="function")
def in_memory_db(
    in_memory_uow_factory: Callable[[], InMemoryUnitOfWork],
    in_memory_storage: InMemoryStorage,
) -> InMemoryDB:
    return InMemoryDB(uow_factory=in_memory_uow_factory, storage=in_memory_storage)


@pytest.fixture(scope="function")
def engine(settings: Settings, setup_migrations: None) -> Generator[Engine, None, None]:
    engine = create_engine(url=settings.database_url)

    yield engine

    engine.dispose()


@pytest.fixture(scope="function")
def connection(engine: Engine) -> Generator[Connection, None, None]:
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def session(connection: Connection) -> Generator[Session, None, None]:
    session = Session(bind=connection, join_transaction_mode="create_savepoint")

    yield session

    if session:
        session.close()


@pytest.fixture(scope="function")
def sqlalchemy_uow_factory(
    session: Session,
) -> Callable[[], SQLAlchemyUnitOfWork]:
    return lambda: SQLAlchemyUnitOfWork(session_factory=lambda: session)


@pytest.fixture(scope="function")
def sqlalchemy_db(
    settings: Settings,
    connection: Connection,
    session: Session,
    sqlalchemy_uow_factory: Callable[[], SQLAlchemyUnitOfWork],
) -> SQLAlchemyDB:
    return SQLAlchemyDB(
        uow_factory=sqlalchemy_uow_factory,
        database_url=settings.database_url,
        engine=connection.engine,
        session_factory=lambda: session,
    )


@pytest.fixture(scope="function")
def container_override(
    settings: Settings, request: pytest.FixtureRequest
) -> ContainerOverride:
    match settings.persistence:
        case "in_memory":
            return ContainerOverride(
                in_memory_db=request.getfixturevalue("in_memory_db")
            )
        case "postgresql":
            return ContainerOverride(
                sqlalchemy_db=request.getfixturevalue("sqlalchemy_db")
            )
        case _:
            raise RuntimeError(
                f"error building container override | $PERSISTENCE: {settings.persistence}"
            )


@pytest.fixture(scope="function")
def container(settings: Settings, container_override: ContainerOverride) -> Container:
    return build_container(settings=settings, overrides=container_override)


@pytest.fixture(scope="function")
def fastapi_app(container: Container) -> FastAPI:
    return create_app(container=container)


@pytest.fixture(scope="function")
def fastapi_testclient(fastapi_app: FastAPI) -> TestClient:
    return TestClient(app=fastapi_app, raise_server_exceptions=False)
