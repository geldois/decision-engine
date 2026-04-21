from typing import Any


class PayloadDeserializer:
    @staticmethod
    def deserialize(data: dict[str, Any]) -> dict[str, Any]:
        return data


class PayloadSerializer:
    @staticmethod
    def serialize(payload: dict[str, Any]) -> dict[str, Any]:
        return payload
