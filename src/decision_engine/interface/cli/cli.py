from __future__ import annotations

import os
import time

import uvicorn
from sqlalchemy import create_engine, text
from typer import Typer

from decision_engine.config.bootstrap import load_environment
from decision_engine.infrastructure.config.db import get_database_url

cli = Typer()


@cli.command("dev")
def dev() -> None:
    port = os.getenv("PORT", "8000")
    uvicorn.run("decision_engine.main:app", host="0.0.0.0", port=int(port), reload=True)


@cli.command("run")
def run() -> None:
    port = os.getenv("PORT", "8000")
    uvicorn.run("decision_engine.main:app", host="0.0.0.0", port=int(port))


@cli.command("wait-db")
def wait_db() -> None:
    load_environment()

    for _ in range(60):
        try:
            engine = create_engine(
                get_database_url(),
                pool_pre_ping=True,
                connect_args={"connect_timeout": 3},
            )

            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            print("database ready")  # noqa: T201

            return
        except Exception:
            print("waiting for database...")

            time.sleep(1)

    message = "database not ready"

    raise RuntimeError(message)
