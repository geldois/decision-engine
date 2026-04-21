import os
import socket
import time

import uvicorn
from sqlalchemy import create_engine, text
from typer import Typer

from app.config.bootstrap import load_environment
from app.infrastructure.config.db import build_database_url

cli = Typer()


@cli.command("dev")
def dev() -> None:
    PORT = os.getenv("PORT", 8000)
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(PORT), reload=True)


@cli.command("run")
def run() -> None:
    PORT = os.getenv("PORT", 8000)
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(PORT))


@cli.command("wait-db")
def wait_db() -> None:
    load_environment()

    for _ in range(60):
        try:
            socket.gethostbyname(os.getenv("DB_HOST"))

            engine = create_engine(
                build_database_url(),
                pool_pre_ping=True,
                connect_args={"connect_timeout": 3},
            )

            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            print("database ready")

            return
        except Exception:
            print("waiting for database...")

            time.sleep(1)
    else:
        raise RuntimeError("database not ready")
