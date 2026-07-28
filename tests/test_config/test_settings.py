from __future__ import annotations

import pytest

from decision_engine.config.settings import Settings

# VALID CASES


def test_build_mem_needs_no_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    settings = Settings.build(persistence="mem")

    assert settings.persistence == "mem"
    assert settings.database_url == ""


def test_build_postgresql_reads_database_url_from_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@host/db")

    settings = Settings.build(persistence="postgresql")

    assert settings.persistence == "postgresql"
    assert settings.database_url == "postgresql+psycopg://user:pass@host/db"


def test_build_prefers_explicit_database_url_over_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://env/db")

    settings = Settings.build(
        persistence="postgresql", database_url="postgresql+psycopg://explicit/db"
    )

    assert settings.database_url == "postgresql+psycopg://explicit/db"


def test_build_reads_persistence_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PERSISTENCE", "mem")
    monkeypatch.delenv("DATABASE_URL", raising=False)

    settings = Settings.build()

    assert settings.persistence == "mem"


# INVALID CASES


def test_build_postgresql_without_database_url_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(KeyError, match="DATABASE_URL"):
        Settings.build(persistence="postgresql")


@pytest.mark.parametrize("invalid_persistence", ["sqlite", "", "MEM"])
def test_build_rejects_invalid_persistence(
    invalid_persistence: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("PERSISTENCE", raising=False)

    with pytest.raises(RuntimeError, match=r"invalid \$PERSISTENCE"):
        Settings.build(persistence=invalid_persistence)


def test_build_missing_persistence_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PERSISTENCE", raising=False)

    with pytest.raises(RuntimeError, match=r"invalid \$PERSISTENCE"):
        Settings.build()
