from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal, TypeGuard, get_args

from decision_engine.infrastructure.config.db import build_database_url

EnvType = Literal["dev", "prod", "test"]
PersistenceType = Literal["mem", "postgresql"]


@dataclass(frozen=True)
class Settings:
    env: EnvType
    persistence: PersistenceType
    database_url: str

    @staticmethod
    def _parse_env(env: str | None) -> EnvType:
        args = get_args(EnvType)

        def _is_env(value: str) -> TypeGuard[EnvType]:
            return value in args

        if env is None or not _is_env(value=env):
            message = f"invalid $ENV: {env}"

            raise RuntimeError(message)

        return env

    @staticmethod
    def _parse_persistence(persistence: str | None) -> PersistenceType:
        args = get_args(PersistenceType)

        def _is_persistence(value: str) -> TypeGuard[PersistenceType]:
            return value in args

        if persistence is None or not _is_persistence(value=persistence):
            message = f"invalid $PERSISTENCE: {persistence}"

            raise RuntimeError(message)

        return persistence

    @classmethod
    def build(  # noqa: PLR0913
        cls,
        *,
        env: str | None = None,
        persistence: str | None = None,
        database_url: str | None = None,
        db_prefix: str | None = None,
        db_user: str | None = None,
        db_pass: str | None = None,
        db_host: str | None = None,
        db_port: str | None = None,
        db_name: str | None = None,
    ) -> Settings:
        env = cls._parse_env(env=env or os.getenv("ENV"))
        persistence = cls._parse_persistence(
            persistence=persistence or os.getenv("PERSISTENCE")
        )

        # The in-memory backend touches no database, so it must not demand a DB
        # config: requiring one would force meaningless dummy DB_* vars in mem
        # deployments (e.g. Render free tier) just to satisfy validation.
        resolved_database_url = (
            build_database_url(
                database_url=database_url,
                db_prefix=db_prefix,
                db_user=db_user,
                db_pass=db_pass,
                db_host=db_host,
                db_port=db_port,
                db_name=db_name,
            )
            if persistence == "postgresql"
            else ""
        )

        return cls(env=env, persistence=persistence, database_url=resolved_database_url)
