from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal, TypeGuard, get_args

from decision_engine.infrastructure.config.db import get_database_url

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
    def build(
        cls,
        *,
        env: str | None = None,
        persistence: str | None = None,
        database_url: str | None = None,
    ) -> Settings:
        env = cls._parse_env(env=env or os.getenv("ENV"))
        persistence = cls._parse_persistence(
            persistence=persistence or os.getenv("PERSISTENCE")
        )

        # The in-memory backend touches no database, so it must not demand a
        # DATABASE_URL: requiring one would force a meaningless dummy value in
        # mem deployments (e.g. Render free tier) just to satisfy validation.
        resolved_database_url = (
            (database_url or get_database_url()) if persistence == "postgresql" else ""
        )

        return cls(env=env, persistence=persistence, database_url=resolved_database_url)
