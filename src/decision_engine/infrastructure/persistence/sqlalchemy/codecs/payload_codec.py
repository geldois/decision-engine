from __future__ import annotations


class PayloadDeserializer:
    @staticmethod
    def deserialize(data: dict[str, object]) -> dict[str, object]:
        return data


class PayloadSerializer:
    @staticmethod
    def serialize(payload: dict[str, object]) -> dict[str, object]:
        return payload
