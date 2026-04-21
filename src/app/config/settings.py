from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal, TypeGuard, get_args

from app.infrastructure.config.db import build_database_url

EnvType = Literal["dev", "prod", "test"]
PersistenceType = Literal["in_memory", "postgresql"]


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
            raise RuntimeError(f"invalid $ENV: {env}")

        return env

    @staticmethod
    def _parse_persistence(persistence: str | None) -> PersistenceType:
        args = get_args(PersistenceType)

        def _is_persistence(value: str) -> TypeGuard[PersistenceType]:
            return value in args

        if persistence is None or not _is_persistence(value=persistence):
            raise RuntimeError(f"invalid $PERSISTENCE: {persistence}")

        return persistence

    @classmethod
    def build(
        cls,
        *,
        env: str | None = None,
        persistence: str | None = None,
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
        database_url = build_database_url(
            db_prefix=db_prefix,
            db_user=db_user,
            db_pass=db_pass,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
        )

        return cls(env=env, persistence=persistence, database_url=database_url)
