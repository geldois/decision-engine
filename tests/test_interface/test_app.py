from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest
    from fastapi.testclient import TestClient

    from decision_engine.config.container import Container

# VALID CASES


def test_root_redirects_to_docs(fastapi_testclient: TestClient) -> None:
    response = fastapi_testclient.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_health_returns_200_when_database_is_reachable(
    fastapi_testclient: TestClient,
) -> None:
    response = fastapi_testclient.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# INVALID CASES


def test_health_returns_503_when_database_is_unreachable(
    container: Container,
    fastapi_testclient: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(container.db, "check_health", lambda: False)

    response = fastapi_testclient.get("/health")

    assert response.status_code == 503
    assert response.json()["detail"]
