from __future__ import annotations

import pytest

from decision_engine.infrastructure.persistence.sqlalchemy.codecs.payload_codec import (
    PayloadDeserializer,
    PayloadSerializer,
)


@pytest.fixture
def payload() -> dict[str, object]:
    return {"test": True, "int": 0, "str": "Hello World!"}


# VALID CASES


def test_payload_codec_roundtrip_preserves_structure(
    payload: dict[str, object],
) -> None:
    encoded = PayloadSerializer.serialize(payload=payload)
    decoded = PayloadDeserializer.deserialize(data=encoded)

    assert decoded == payload
