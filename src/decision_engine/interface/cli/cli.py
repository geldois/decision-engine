from __future__ import annotations

import os
import time

import structlog
import uvicorn
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from typer import Typer

from decision_engine.config.bootstrap import load_environment
from decision_engine.infrastructure.config.db import get_database_url

cli = Typer()
logger = structlog.get_logger()

_WAIT_DB_ATTEMPTS = 60
_WAIT_DB_CONNECT_TIMEOUT = 3

# Bind on all interfaces: the process runs inside a container whose port is
# published explicitly, so 127.0.0.1 would leave it unreachable from the host.
_HOST = "0.0.0.0"  # noqa: S104


@cli.command("dev")
def dev() -> None:
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("decision_engine.main:app", host=_HOST, port=port, reload=True)


@cli.command("run")
def run() -> None:
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("decision_engine.main:app", host=_HOST, port=port)


@cli.command("wait-db")
def wait_db() -> None:
    load_environment()

    for _ in range(_WAIT_DB_ATTEMPTS):
        try:
            engine = create_engine(
                get_database_url(),
                pool_pre_ping=True,
                connect_args={"connect_timeout": _WAIT_DB_CONNECT_TIMEOUT},
            )

            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except OperationalError:
            logger.info("database.waiting")

            time.sleep(1)
        else:
            logger.info("database.ready")

            return

    message = "database not ready"

    raise RuntimeError(message)
