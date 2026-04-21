from typing import Any

import pytest

from app.infrastructure.persistence.sqlalchemy.codecs.payload_codec import (
    PayloadDeserializer,
    PayloadSerializer,
)


@pytest.fixture(scope="function")
def payload() -> dict[str, Any]:
    return {"test": True, "int": 0, "str": "Hello World!"}


# VALID CASES


def test_payload_codec_roundtrip_preserves_structure(
    payload: dict[str, Any]
) -> None:
    encoded = PayloadSerializer.serialize(payload=payload)
    decoded = PayloadDeserializer.deserialize(data=encoded)

    assert decoded == payload
