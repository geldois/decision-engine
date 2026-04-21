import pytest


@pytest.fixture(scope="function")
def persistence() -> str:
    return "postgresql"
