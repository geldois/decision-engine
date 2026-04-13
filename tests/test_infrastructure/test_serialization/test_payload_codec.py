import app.infrastructure.serialization.payload_codec as PayloadCodec


# ==========
# valid cases
# ==========
def test_payload_codec_serializes_payload() -> None:
    payload = {"test": True, "int": 0, "str": "Hello World!"}

    data = PayloadCodec.serialize(payload=payload)

    assert data == '{"test": true, "int": 0, "str": "Hello World!"}'


def test_payload_codec_deserializes_payload() -> None:
    payload = {"test": True, "int": 0, "str": "Hello World!"}

    data = PayloadCodec.serialize(payload=payload)

    assert PayloadCodec.deserialize(payload=data) == payload
