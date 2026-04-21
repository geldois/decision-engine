from collections.abc import Callable
from dataclasses import replace
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.config.container import Container
from app.interface.http.app import create_app


@pytest.fixture(scope="function")
def broken_fastapi_testclient_factory(
    container: Container,
) -> Callable[..., TestClient]:
    def _broken_fastapi_testclient_factory(**use_cases: Any) -> TestClient:
        broken_use_cases = replace(container.use_cases, **use_cases)
        broken_container = replace(container, use_cases=broken_use_cases)
        broken_app = create_app(container=broken_container)

        return TestClient(app=broken_app, raise_server_exceptions=False)

    return _broken_fastapi_testclient_factory
