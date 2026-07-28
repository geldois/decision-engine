from __future__ import annotations

from decision_engine.config.bootstrap import load_environment, run_migrations
from decision_engine.config.settings import Settings
from decision_engine.interface.http.app import create_app

load_environment()

# The mem backend has no schema to migrate; running Alembic there would build a
# real engine and fail (no reachable/valid database). Gate migrations on the
# persistence backend so mem deployments boot without any DB config.
if Settings.build().persistence == "postgresql":
    run_migrations()

app = create_app()
